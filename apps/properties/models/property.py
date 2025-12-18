from django.db import models
import uuid

class Property(models.Model):
    """
    Represents a single PG branch.
    Covers: Advanced Feature 1 (Multi-Property Management)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, db_index=True)
    address = models.TextField()
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='owned_properties', limit_choices_to={'role': 'SUPERADMIN'})
    manager = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_properties', limit_choices_to={'role': 'MANAGER'})
    
    # USP 13: Hygiene Scorecard - Public Display
    current_hygiene_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, help_text="Current hygiene rating out of 5", db_index=True)
    
    # Multi-language support
    preferred_language = models.CharField(max_length=10, choices=[('EN', 'English'), ('HI', 'Hindi'), ('TE', 'Telugu')], default='EN')
    
    # Property metadata
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
