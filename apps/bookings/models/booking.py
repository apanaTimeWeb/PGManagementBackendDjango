from django.db import models
import uuid

class Booking(models.Model):
    """
    Manages a tenant's stay in a specific bed.
    Covers: Module 3 (Tenant Lifecycle), USPs 7, 8, 9
    """
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        NOTICE_PERIOD = 'NOTICE_PERIOD', 'On Notice Period'
        EXITED = 'EXITED', 'Exited'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='bookings', limit_choices_to={'role': 'TENANT'})
    bed = models.ForeignKey('properties.Bed', on_delete=models.PROTECT, related_name='bookings')
    
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True, db_index=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)

    # USP 8: Zero-Deposit Option
    is_zero_deposit = models.BooleanField(default=False, db_index=True)
    fintech_partner_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    fintech_loan_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    # USP 9: Digital Notice Period & Auto Refund
    notice_given_date = models.DateField(null=True, blank=True, db_index=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_processed_date = models.DateField(null=True, blank=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['status', 'start_date', 'end_date'])
        ]

    def __str__(self):
        return f"Booking for {self.tenant.username} in {self.bed}"
