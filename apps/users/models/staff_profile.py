from django.db import models
import uuid
from .custom_user import CustomUser

class StaffProfile(models.Model):
    """
    Extended profile for staff members.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile', limit_choices_to={'role': 'STAFF'})
    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True)
    
    role = models.CharField(max_length=50, choices=[('COOK', 'Cook'), ('GUARD', 'Guard'), ('CLEANER', 'Cleaner'), ('MANAGER', 'Manager'), ('MAINTENANCE', 'Maintenance')])
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    police_verification_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('VERIFIED', 'Verified')], default='PENDING')
    
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('RESIGNED', 'Resigned'), ('TERMINATED', 'Terminated')], default='ACTIVE')
    
    # Banking
    bank_account_number = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.user.username}"
