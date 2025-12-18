from django.db import models
import uuid

class Bed(models.Model):
    """
    The smallest bookable unit in a room.
    Covers: USPs 3, 5
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='beds')
    bed_label = models.CharField(max_length=5, help_text="e.g., A, B, Upper, Lower")
    
    # USP 3: Live "Vacant Bed" Public Link
    public_uid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, help_text="Public link UUID for sharing bed availability without login")
    is_occupied = models.BooleanField(default=False, db_index=True)
    
    # USP 5: Smart Electricity Billing (IoT)
    iot_meter_id = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)

    class Meta:
        unique_together = ('room', 'bed_label')
        indexes = [
             models.Index(fields=['room', 'is_occupied'])
        ]

    def __str__(self):
        return f"Bed {self.bed_label}"

class ElectricityReading(models.Model):
    """
    IoT meter readings for individual bed energy consumption.
    Covers: USP 5 (Smart Electricity Billing)
    """
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='electricity_readings')
    meter_id = models.CharField(max_length=50, db_index=True)
    reading_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [models.Index(fields=['meter_id', 'timestamp'])]

    def __str__(self):
        return f"{self.meter_id} - {self.reading_kwh} units"
