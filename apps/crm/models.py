from django.db import models
import uuid

class Lead(models.Model):
    """
    Tracks enquiries from potential tenants.
    Covers: Advanced Feature 5 (CRM & Lead Management)
    """
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        VISITED = 'VISITED', 'Visited'
        CONVERTED = 'CONVERTED', 'Converted'
        LOST = 'LOST', 'Lost'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(null=True, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    converted_tenant = models.OneToOneField('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_record', help_text="Linked tenant profile if converted.")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Lead: {self.full_name} for {self.property.name}"
