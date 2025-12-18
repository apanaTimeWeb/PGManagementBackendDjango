from django.db import models
import uuid

class Room(models.Model):
    """
    Represents a room within a PG property.
    Covers: Module 2 (Property & Rooms)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10, db_index=True)
    capacity = models.PositiveIntegerField(default=2, help_text="Number of beds in the room.", db_index=True)
    
    # USP 4: Dynamic Pricing Engine
    base_rent_per_bed = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    
    # Room amenities for better filtering
    has_ac = models.BooleanField(default=False, db_index=True)
    has_balcony = models.BooleanField(default=False, db_index=True)
    has_attached_bathroom = models.BooleanField(default=False, db_index=True)
    floor_number = models.IntegerField(default=0, db_index=True)

    class Meta:
        unique_together = ('property', 'room_number')
        indexes = [
            models.Index(fields=['property', 'has_ac']),
            models.Index(fields=['property', 'base_rent_per_bed'])
        ]

    def __str__(self):
        return f"Room {self.room_number}"
