from django.db import models

class EntryLog(models.Model):
    """
    Biometric/QR code entry and exit logs.
    Covers: USP 12 (Biometric/QR Entry + Night Alert)
    """
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    direction = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')], db_index=True)
    entry_method = models.CharField(max_length=20, choices=[('BIOMETRIC', 'Biometric'), ('QR', 'QR Code'), ('MANUAL', 'Manual')], default='MANUAL')
    is_late_entry = models.BooleanField(default=False, db_index=True)
    parent_alert_sent = models.BooleanField(default=False)
