# Importing APIView base class for creating class-based views in DRF
from rest_framework.views import APIView
# Importing Response object to return HTTP responses
from rest_framework.response import Response
# Importing status codes (e.g., 201 Created, 400 Bad Request)
from rest_framework import status
# Importing transaction module to handle database transactions (atomic operations)
from django.db import transaction
# Importing the serializer we created to validate user inputs
from apps.users.serializers.auth_serializers import UserRegistrationSerializer
# Importing all the user-related models needed for profile creation and logging
from apps.users.models import CustomUser, TenantProfile, StaffProfile, OwnerProfile, ActivityLog

from rest_framework.permissions import AllowAny

# Define RegisterView class handling User Registration logic
class RegisterView(APIView):
    permission_classes = [AllowAny]
    # Handle POST requests (creating new resources)
    def post(self, request):
        # Initialize serializer with the data sent in the request body
        serializer = UserRegistrationSerializer(data=request.data)
        
        # Check if the data is valid (based on model fields and custom validators)
        if serializer.is_valid():
            try:
                # Start an atomic transaction block. If any error occurs inside, database changes are rolled back.
                with transaction.atomic():
                    # Save the user instance using the serializer's create method
                    user = serializer.save()
                    
                    # --- Manual Profile Creation Logic (Replaces Signals) ---
                    # Check the role of the newly created user to determine which profile to create
                    
                    # If the user is a TENANT
                    if user.role == CustomUser.Roles.TENANT:
                        # Create an empty TenantProfile linked to this user
                        TenantProfile.objects.create(user=user)
                        
                    # If the user is a MANAGER or STAFF member
                    elif user.role in [CustomUser.Roles.MANAGER, CustomUser.Roles.STAFF]:
                        # Create an empty StaffProfile linked to this user
                        StaffProfile.objects.create(user=user)
                        
                    # If the user is a SUPERADMIN (Owner)
                    elif user.role == CustomUser.Roles.SUPERADMIN:
                        # Create an empty OwnerProfile linked to this user
                        OwnerProfile.objects.create(user=user)
                    
                    # --- Activity Logging ---
                    # Log this registration event in the database for audit purposes
                    ActivityLog.objects.create(
                        user=user,  # The user who performed the action (or related to it)
                        action="USER_REGISTERED",  # Short code for the action
                        details=f"User {user.username} registered with role {user.role}",  # Readable description
                        ip_address=request.META.get('REMOTE_ADDR')  # Capture user's IP address
                    )

                    # Return a success response with user details
                    return Response({
                        "success": True,  # Boolean flag for frontend ease
                        "message": "User registered successfully",  # Human-readable message
                        "user": {  # Return key user details (excluding sensitive data like password)
                            "id": str(user.id),  # Convert UUID to string
                            "username": user.username,
                            "role": user.role
                        }
                    }, status=status.HTTP_201_CREATED)  # HTTP 201 Created status
                    
            except Exception as e:
                # If any unexpected error occurs during the transaction, return 400 Bad Request
                return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

        # If serializer validation fails (e.g., duplicate email), return the errors with 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Login View Implementation ---
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers.auth_serializers import LoginSerializer
from django.db.models import Q
from django.core.cache import cache
from datetime import datetime

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # 1. Rate Limiting Check
        ip_address = request.META.get('REMOTE_ADDR')
        lockout_key = f"login_lockout_{ip_address}"
        attempts_key = f"login_attempts_{ip_address}"

        if cache.get(lockout_key):
             return Response(
                {"success": False, "message": "Account locked due to too many failed attempts. Try again in 30 minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username_input = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # 2. Resolve User (Username/Email/Phone)
        user = None
        try:
            user = CustomUser.objects.get(
                Q(username=username_input) | 
                Q(email=username_input) | 
                Q(phone_number=username_input)
            )
        except CustomUser.DoesNotExist:
            pass # User will remain None, authentication will fail below

        # 3. Authenticate
        # We need to pass the actual username to authenticate if we found the user
        if user:
            user = authenticate(username=user.username, password=password)

        if user is None:
            # Increment failed attempts
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, 900) # 15 minutes window

            if attempts >= 5:
                cache.set(lockout_key, True, 1800) # Lock for 30 minutes
                return Response(
                    {"success": False, "message": "Too many failed attempts. Account locked for 30 minutes."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            return Response(
                {"success": False, "message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 4. Check Active/Blocked Status
        if not user.is_active:
             return Response(
                {"success": False, "message": "Account is disabled."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 5. Reset Failed Attempts on Success
        cache.delete(attempts_key)
        cache.delete(lockout_key)

        # 6. Generate Tokens
        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role # Add custom claim
        
        # 7. Update Last Login
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # 8. Log Activity
        ActivityLog.objects.create(
            user=user,
            action="USER_LOGIN",
            details=f"User {user.username} logged in successfully",
            ip_address=ip_address
        )

        # 9. Response
        return Response({
            "success": True,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)


# --- Aadhaar Upload View ---
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.auth_serializers import AadhaarUploadSerializer
from apps.users.utils import encrypt_aadhaar, generate_police_verification_pdf
import uuid

class AadhaarUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # 1. Role Check
        if user.role != CustomUser.Roles.TENANT:
             return Response(
                {"success": False, "message": "Only tenants can upload Aadhaar."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = AadhaarUploadSerializer(data=request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
        aadhaar_number = serializer.validated_data['aadhaar_number']
        
        # 2. Check Duplicates (In real world, need blind index or similar. For now, check if encrypted matches any?)
        # Since encryption is randomized (IV) with Fernet, we can't search directly.
        # For this demo, we'll skip global uniqueness check on ENCRYPTED field or assume we decrypt all (slow)
        # OR we just rely on profile check.
        
        # Check if user already uploaded
        try:
            profile = user.tenant_profile
        except TenantProfile.DoesNotExist:
             return Response(
                {"success": False, "message": "Tenant profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if profile.aadhaar_number:
             return Response(
                {"success": False, "message": "Aadhaar already uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Encrypt 
        encrypted_aadhaar = encrypt_aadhaar(aadhaar_number)
        
        # 4. Mock S3 Upload (Images)
        # We just generate a fake URL for now as we don't have AWS creds
        fake_s3_url_front = f"https://s3.amazonaws.com/pg-management/aadhaar/{user.id}/front_{uuid.uuid4()}.jpg"
        fake_s3_url_back = f"https://s3.amazonaws.com/pg-management/aadhaar/{user.id}/back_{uuid.uuid4()}.jpg"
        
        # 5. Generate Police Verification Form
        pdf_path = generate_police_verification_pdf({
            'username': user.username,
            'full_name': user.get_full_name() or user.username,
            'phone': user.phone_number,
            'aadhaar_last_4': aadhaar_number[-4:],
            'address': 'See attached ID proof'
        })
        
        # 6. Update Profile
        profile.aadhaar_number = encrypted_aadhaar
        profile.aadhaar_url = f"{fake_s3_url_front},{fake_s3_url_back}" # Storing both as comma sep
        profile.police_verification_status = 'SUBMITTED'
        profile.save()
        
        # 7. Audit Log
        ActivityLog.objects.create(
            user=user,
            action="AADHAAR_UPLOAD",
            details="Aadhaar uploaded and police verification form generated.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            "success": True,
            "message": "Aadhaar uploaded and police verification triggered.",
            "verification_status": "SUBMITTED",
            "form_url": pdf_path # Sending local path for verification
        }, status=status.HTTP_200_OK)


