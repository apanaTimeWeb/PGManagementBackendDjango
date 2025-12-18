from django.db import models
import uuid

class SOSAlert(models.Model):
    """
    Emergency SOS alert tracking for tenant safety.
    Covers: USP 11 (SOS Alert System)
    """
    class Status(models.TextChoices):
        TRIGGERED = 'TRIGGERED', 'Triggered'
        RESPONDING = 'RESPONDING', 'Manager Responding'
        RESOLVED = 'RESOLVED', 'Resolved'
        FALSE_ALARM = 'FALSE_ALARM', 'False Alarm'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='sos_alerts', limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.PROTECT)
    
    # Location data
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS longitude")
    location_accuracy = models.IntegerField(null=True, blank=True, help_text="GPS accuracy in meters")
    
    # Alert details
    message = models.TextField(blank=True, help_text="Optional emergency message from tenant")
    device_info = models.JSONField(default=dict, blank=True, help_text="Device type, OS, app version")
    
    # Response tracking
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIGGERED, db_index=True)
    triggered_at = models.DateTimeField(auto_now_add=True, db_index=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True, help_text="When manager/security acknowledged")
    resolved_at = models.DateTimeField(null=True, blank=True)
    response_time_seconds = models.IntegerField(null=True, blank=True, help_text="Time to first response in seconds")
    
    # Responders
    first_responder = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='responded_sos_alerts', help_text="First person to respond to the alert")
    
    # Notifications sent
    manager_notified = models.BooleanField(default=False)
    parent_notified = models.BooleanField(default=False)
    security_notified = models.BooleanField(default=False)
    owner_notified = models.BooleanField(default=False)
    
    # Resolution
    resolution_notes = models.TextField(blank=True, help_text="How incident was resolved")
    is_genuine_emergency = models.BooleanField(null=True, blank=True, help_text="True if genuine, False if false alarm, Null if undetermined", db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'triggered_at']),
            models.Index(fields=['property', 'status']),
        ]
        ordering = ['-triggered_at']
    
    def __str__(self):
        return f"SOS Alert by {self.tenant.username} at {self.triggered_at}"
