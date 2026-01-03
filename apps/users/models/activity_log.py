from django.db import models
import uuid
from .custom_user import CustomUser

class ActivityLog(models.Model):
    """
    Tracks all critical user actions for audit trail.
    Ref: Table ActivityLog in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    severity = models.CharField(max_length=20, choices=[('INFO', 'Info'), ('WARNING', 'Warning'), ('CRITICAL', 'Critical')], default='INFO')
    entity_type = models.CharField(max_length=50, null=True, blank=True, help_text="PAYMENT | TENANT | PROPERTY | ROOM")
    entity_id = models.UUIDField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['entity_type', 'entity_id'])
        ]

    def __str__(self):
        return f"{self.action} by {self.user.username} at {self.timestamp}"
