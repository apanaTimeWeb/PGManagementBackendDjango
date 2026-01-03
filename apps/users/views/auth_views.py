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

# Define RegisterView class handling User Registration logic
class RegisterView(APIView):
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
