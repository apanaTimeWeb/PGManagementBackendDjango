from rest_framework.views import APIView
from rest_framework.response import Response

# Placeholder views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from apps.users.serializers.auth_serializers import UserRegistrationSerializer
from apps.users.models import CustomUser, TenantProfile, StaffProfile, OwnerProfile, ActivityLog

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    
                    # Manual Profile Creation (No Signals)
                    if user.role == CustomUser.Roles.TENANT:
                        TenantProfile.objects.create(user=user)
                    elif user.role in [CustomUser.Roles.MANAGER, CustomUser.Roles.STAFF]:
                        StaffProfile.objects.create(user=user)
                    elif user.role == CustomUser.Roles.SUPERADMIN:
                        OwnerProfile.objects.create(user=user)
                    
                    # Log Activity
                    ActivityLog.objects.create(
                        user=user,
                        action="USER_REGISTERED",
                        details=f"User {user.username} registered with role {user.role}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )

                    return Response({
                        "success": True,
                        "message": "User registered successfully",
                        "user": {
                            "id": str(user.id),
                            "username": user.username,
                            "role": user.role
                        }
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
