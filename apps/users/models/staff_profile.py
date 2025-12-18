from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import CustomUser

class StaffProfile(models.Model):
    """
    Extended profile for staff members (cook, guard, etc.).
    Covers: Advanced Feature 3 (Staff & Payroll)
    """
    class StaffRoles(models.TextChoices):
        COOK = 'COOK', _('Cook')
        GUARD = 'GUARD', _('Security Guard')
        CLEANER = 'CLEANER', _('Cleaner')
        OTHER = 'OTHER', _('Other')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'STAFF'})
    staff_role = models.CharField(max_length=20, choices=StaffRoles.choices, db_index=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salary per day for payroll calculation.")
    assigned_property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    joining_date = models.DateField(db_index=True)

    def __str__(self):
        return f"Staff Profile: {self.user.username}"
