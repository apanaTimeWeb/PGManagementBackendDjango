from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUser(AbstractUser):
    """
    Central user model for authentication and role management.
    Covers: Module 1 (User Roles & Auth)
    """
    class Roles(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', _('Super Admin (Owner)')
        MANAGER = 'MANAGER', _('Manager (Warden)')
        TENANT = 'TENANT', _('Tenant (Student)')
        PARENT = 'PARENT', _('Parent (Guardian)')
        STAFF = 'STAFF', _('Staff (Cook, Guard)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.TENANT, db_index=True)
    phone_number = models.CharField(max_length=15, unique=True, help_text="Used for login and notifications.", db_index=True)
    email = models.EmailField(unique=True, null=True, blank=True, db_index=True)
    profile_photo_url = models.TextField(null=True, blank=True, help_text="External URL or path") 
    
    # DBML Alignment
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    # Technical Feature 6: Localization
    language_code = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('ta', 'Tamil'), ('te', 'Telugu'), ('kn', 'Kannada'), ('bn', 'Bengali')], default='en')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
