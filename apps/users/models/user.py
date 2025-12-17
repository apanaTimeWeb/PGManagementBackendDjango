from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=[
        ('tenant', 'Tenant'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('admin', 'Admin')
    ], default='tenant')
    is_verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=5, default='en')
    
    def __str__(self):
        return self.username