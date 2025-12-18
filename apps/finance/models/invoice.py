from django.db import models
import uuid

class Invoice(models.Model):
    """
    Monthly invoice for tenants.
    Covers: Module 4 (Finance)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.PROTECT)
    issue_date = models.DateField(auto_now_add=True, db_index=True)
    due_date = models.DateField(db_index=True)
    
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mess_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    electricity_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_paid = models.BooleanField(default=False, db_index=True)
    paid_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for {self.booking.tenant.username} - {self.issue_date.strftime('%B %Y')}"
