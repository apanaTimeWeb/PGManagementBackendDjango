from django.db import models
import uuid

class SubscriptionPlan(models.Model):
    """
    Defines different subscription tiers for PG owners.
    Covers: Technical Feature 8 (The SaaS Angle)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, help_text="e.g., Basic, Gold, Platinum", db_index=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    max_properties = models.IntegerField(help_text="Maximum number of PG branches allowed")
    max_rooms = models.IntegerField(help_text="Maximum total rooms across all properties")
    features = models.JSONField(default=dict, help_text="Feature flags: {'crm': true, 'alumni': false}")
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

class PropertySubscription(models.Model):
    """
    Tracks subscription status for each property owner.
    Covers: Technical Feature 8 (The SaaS Angle)
    """
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'
        TRIAL = 'TRIAL', 'Trial'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'SUPERADMIN'})
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIAL, db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    auto_renew = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner.username} - {self.plan.name}"

class AppVersion(models.Model):
    """
    Manages app versions for forced updates.
    Covers: Technical Feature 5 (Version Control & App Updates)
    """
    platform = models.CharField(max_length=10, choices=[('ANDROID', 'Android'), ('IOS', 'iOS')], db_index=True)
    version_code = models.IntegerField(help_text="e.g., 102")
    version_name = models.CharField(max_length=20, help_text="e.g., 1.0.2")
    is_mandatory = models.BooleanField(default=False, help_text="Force update required?")
    release_date = models.DateField()
    
    def __str__(self):
        return f"{self.platform} - {self.version_name}"
