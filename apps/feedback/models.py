from django.db import models
import uuid

class ComplaintFeedback(models.Model):
    """
    Tenant feedback on resolved complaints.
    Covers: Technical Feature 9 (Feedback & Rating Loop)
    """
    complaint = models.OneToOneField('operations.Complaint', on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(help_text="Rating from 1 to 5", db_index=True)
    feedback_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Feedback for Complaint #{self.complaint.id}"

class MessFeedback(models.Model):
    """
    Daily feedback on mess food quality.
    Covers: Technical Feature 9 (Feedback & Rating Loop)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    menu = models.ForeignKey('mess.MessMenu', on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=[('BREAKFAST', 'Breakfast'), ('LUNCH', 'Lunch'), ('DINNER', 'Dinner')], db_index=True)
    rating = models.IntegerField(help_text="Rating from 1 to 5", db_index=True)
    feedback_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Mess Feedback by {self.tenant.username} on {self.menu.date}"
