from django.db import models
import uuid
from .custom_user import CustomUser

class OwnerProfile(models.Model):
    """
    Business profile for PG Owners (SuperAdmins).
    Ref: Table OwnerProfile in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owner_profile')
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    pan_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    business_established_date = models.DateField(null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    total_properties_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
