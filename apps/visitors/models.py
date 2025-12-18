from django.db import models
import uuid

class VisitorRequest(models.Model):
    """
    Tracks visitor entry requests and approvals.
    Covers: Advanced Feature 6 (Visitor Management)
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CHECKED_OUT = 'CHECKED_OUT', 'Checked Out'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='visitor_requests', limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=15, db_index=True)
    visitor_photo = models.ImageField(upload_to='visitors/', null=True, blank=True)
    purpose = models.CharField(max_length=255)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True, db_index=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    guard = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_visitors', limit_choices_to={'role': 'STAFF'})

    def __str__(self):
        return f"Visitor {self.visitor_name} for {self.tenant.username}"
