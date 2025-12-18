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
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # USP 11: Women Safety & SOS Button
    sos_contact_number = models.CharField(max_length=15, null=True, blank=True, help_text="Emergency contact for SOS alerts.")
    
    # Technical Feature 6: Localization (Multi-Language Support)
    preferred_language = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('ta', 'Tamil'), ('te', 'Telugu'), ('kn', 'Kannada'), ('bn', 'Bengali')], default='en', help_text="User's preferred language for app interface.")

    # Added verification flag frequently used in login logic
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'), db_index=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"