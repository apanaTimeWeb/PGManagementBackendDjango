from django.db import models
import uuid
from .custom_user import CustomUser

class TenantProfile(models.Model):
    """
    Extended profile for tenants (students).
    Covers: USPs 1, 2, 6, 8, 10, 15
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tenant_profile', limit_choices_to={'role': 'TENANT'})
    
    # Current Residence (Optimization: Denormalized FKs)
    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_tenants')
    room = models.ForeignKey('properties.Room', on_delete=models.SET_NULL, null=True, blank=True)
    bed = models.ForeignKey('properties.Bed', on_delete=models.SET_NULL, null=True, blank=True)
    
    # KYC Details (USP #2)
    aadhaar_number = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Stores encrypted Aadhaar (Fernet produces ~200 chars)
    aadhaar_url = models.TextField(null=True, blank=True)
    id_proof_type = models.CharField(max_length=50, choices=[('AADHAR', 'Aadhar'), ('PAN', 'PAN'), ('PASSPORT', 'Passport'), ('DRIVING_LICENSE', 'Driving License')], null=True, blank=True)
    id_proof_url = models.TextField(null=True, blank=True)
    police_verification_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUBMITTED', 'Submitted'), ('VERIFIED', 'Verified'), ('REJECTED', 'Rejected')], default='PENDING', db_index=True)
    
    # Financial & Scoring
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pg_credit_score = models.IntegerField(default=700, help_text="USP #10: Score for conduct and payments")
    
    # Guardian Info (Fallback if Parent mapped User not available)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Education
    college_name = models.CharField(max_length=255, null=True, blank=True)
    course_name = models.CharField(max_length=255, null=True, blank=True)
    education_details = models.TextField(null=True, blank=True)
    
    # Stay Dates
    check_in_date = models.DateField(null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)
    notice_period_days = models.IntegerField(default=30)
    
    # Photos (JSON Arrays)
    check_in_photos = models.JSONField(default=list, blank=True)
    room_inspection_photos = models.JSONField(default=list, blank=True)
    
    # AI Matching Preferences (USP #6)
    sleep_schedule = models.CharField(max_length=20, choices=[('EARLY_BIRD', 'Early Bird'), ('NIGHT_OWL', 'Night Owl')], null=True, blank=True)
    dietary_preference = models.CharField(max_length=20, choices=[('VEG', 'Veg'), ('NON_VEG', 'Non Veg'), ('VEGAN', 'Vegan')], null=True, blank=True)
    cleanliness_level = models.CharField(max_length=20, choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], null=True, blank=True)
    smoking_habit = models.CharField(max_length=20, choices=[('SMOKER', 'Smoker'), ('NON_SMOKER', 'Non Smoker')], null=True, blank=True)
    study_hours = models.CharField(max_length=20, choices=[('DAY', 'Day'), ('NIGHT', 'Night')], null=True, blank=True)
    noise_tolerance = models.CharField(max_length=20, choices=[('HIGH', 'High'), ('LOW', 'Low')], null=True, blank=True)
    personality_type = models.CharField(max_length=20, choices=[('INTROVERT', 'Introvert'), ('EXTROVERT', 'Extrovert')], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
