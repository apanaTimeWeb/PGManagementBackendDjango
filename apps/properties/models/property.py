from django.db import models
import uuid

class Property(models.Model):
    """
    Represents a single PG branch.
    Ref: Table Property in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Using string reference to avoid circular import if needed (but users model exists so strict import ok if careful)
    # However, to avoid circular dependency issues at module level:
    owner = models.ForeignKey('users.OwnerProfile', on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    
    # Business Details
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    pan_number = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    
    # Specs
    total_floors = models.IntegerField(default=1)
    property_type = models.CharField(max_length=20, choices=[('BOYS', 'Boys'), ('GIRLS', 'Girls'), ('CO_ED', 'Co-Ed')])
    
    # Geo
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    
    # Media
    images_url = models.JSONField(default=list, blank=True, help_text="List of image URLs")
    
    # Metrics
    monthly_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    hygiene_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    # Features
    iot_enabled = models.BooleanField(default=False, help_text="USP #5")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.city}"
