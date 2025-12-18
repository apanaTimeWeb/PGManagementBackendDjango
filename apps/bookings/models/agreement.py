from django.db import models
from .booking import Booking

class DigitalAgreement(models.Model):
    """
    Stores e-signed rental agreements.
    Covers: USP 7 (Digital Agreement)
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    agreement_file = models.FileField(upload_to='agreements/')
    is_signed = models.BooleanField(default=False, db_index=True)
    signed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Agreement for {self.booking}"
