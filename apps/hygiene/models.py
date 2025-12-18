from django.db import models
import uuid

class HygieneInspection(models.Model):
    """
    Weekly hygiene inspection records.
    Covers: USP 13 (Hygiene Scorecard)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='hygiene_inspections')
    inspection_date = models.DateField(db_index=True)
    inspector = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role__in': ['MANAGER', 'SUPERADMIN']})
    
    cleanliness_score = models.IntegerField(help_text="Score out of 10")
    kitchen_score = models.IntegerField(help_text="Score out of 10")
    bathroom_score = models.IntegerField(help_text="Score out of 10")
    common_area_score = models.IntegerField(help_text="Score out of 10")
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, help_text="Average rating out of 5", db_index=True)
    photos = models.JSONField(default=list, help_text="List of photo URLs")
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Hygiene Inspection - {self.property.name} on {self.inspection_date}"
