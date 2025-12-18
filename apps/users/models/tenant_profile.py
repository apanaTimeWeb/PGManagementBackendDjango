from django.db import models
from .user import CustomUser

class TenantProfile(models.Model):
    """
    Extended profile for tenants (students).
    Covers: USPs 1, 2, 6, 8, 10, 15
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'TENANT'})
    
    # USP 1: Parent Portal Access
    guardian = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards', limit_choices_to={'role': 'PARENT'})
    
    # USP 2: Aadhaar + Police Verification
    aadhaar_number = models.CharField(max_length=12, null=True, blank=True, db_index=True)
    police_verification_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUBMITTED', 'Submitted'), ('VERIFIED', 'Verified')], default='PENDING', db_index=True)
    
    # USP 10: Tenant Credit Score
    credit_score = models.IntegerField(default=700, help_text="Score for timely payments and good conduct.")
    
    # USP 6: AI Compatibility Matching - Detailed Preferences
    sleep_schedule = models.CharField(max_length=20, choices=[('EARLY_BIRD', 'Early Bird'), ('NIGHT_OWL', 'Night Owl'), ('FLEXIBLE', 'Flexible')], null=True, blank=True)
    cleanliness_level = models.CharField(max_length=20, choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], null=True, blank=True)
    noise_tolerance = models.CharField(max_length=20, choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], null=True, blank=True)
    study_hours = models.CharField(max_length=20, choices=[('MORNING', 'Morning'), ('AFTERNOON', 'Afternoon'), ('LATE_NIGHT', 'Late Night'), ('FLEXIBLE', 'Flexible')], null=True, blank=True)
    lifestyle_attributes = models.JSONField(default=dict, blank=True, help_text="Additional attributes for compatibility: {'smoker': false, 'vegetarian': true}")
    
    # USP 15: Smart Mess Wallet
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Tenant Profile: {self.user.username}"
