from django.db import models
import uuid

class Complaint(models.Model):
    """
    Tenant complaint management system.
    Covers: Module 5 (Operations & Safety)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], default='OPEN', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # USP 14: AI Chatbot Integration
    is_raised_by_bot = models.BooleanField(default=False, help_text="True if complaint was raised via WhatsApp AI Bot")

    def __str__(self):
        return f"Complaint #{self.id} by {self.tenant.username}"
