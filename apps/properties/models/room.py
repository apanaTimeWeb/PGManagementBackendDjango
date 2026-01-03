from django.db import models
import uuid
from .property import Property

class Room(models.Model):
    """
    Represents a room within a PG property.
    Ref: Table Room in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=20, choices=[('SINGLE', 'Single'), ('DOUBLE', 'Double'), ('TRIPLE', 'Triple'), ('DORMITORY', 'Dormitory')])
    
    # Financials
    base_rent = models.DecimalField(max_digits=10, decimal_places=2)
    current_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    electricity_reading = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Amenities & Specs
    has_ac = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=True)
    has_attached_bathroom = models.BooleanField(default=False)
    window_count = models.IntegerField(default=1)
    carpet_area_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    images_url = models.JSONField(default=list, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('AVAILABLE', 'Available'), ('OCCUPIED', 'Occupied'), ('MAINTENANCE', 'Maintenance')], default='AVAILABLE')

    class Meta:
        unique_together = ('property', 'room_number')

    def __str__(self):
        return f"{self.room_number} ({self.type})"
