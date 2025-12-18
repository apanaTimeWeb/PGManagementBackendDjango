from django.db import models
import uuid

class AlumniProfile(models.Model):
    """
    Extended profile for ex-tenants (alumni).
    Covers: Advanced Feature 9 (Alumni Network)
    """
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, primary_key=True)
    current_company = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    current_position = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    is_open_to_referrals = models.BooleanField(default=False, db_index=True)
    exit_date = models.DateField(help_text="Date when tenant left the PG", db_index=True)
    properties_stayed = models.ManyToManyField('properties.Property', related_name='alumni')

    def __str__(self):
        return f"Alumni: {self.user.username}"

class JobReferral(models.Model):
    """
    Job referral requests between alumni and current tenants.
    Covers: Advanced Feature 9 (Alumni Network)
    """
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='referral_requests')
    alumni = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='referrals_given')
    company_name = models.CharField(max_length=100, db_index=True)
    position = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Referral request from {self.requester.username} to {self.alumni.username}"
