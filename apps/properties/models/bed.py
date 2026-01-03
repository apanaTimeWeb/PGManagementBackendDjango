from django.db import models
import uuid
from .room import Room

class Bed(models.Model):
    """
    The smallest bookable unit.
    Ref: Table Bed in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    label = models.CharField(max_length=10, help_text="A, B, C...")
    is_occupied = models.BooleanField(default=False)
    
    # USP Integrations
    iot_meter_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="USP #5")
    public_uid = models.UUIDField(default=uuid.uuid4, unique=True, help_text="USP #3: Public share link")
    
    current_tenant = models.OneToOneField('users.TenantProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_bed')
    last_occupied_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('room', 'label')

    def __str__(self):
        return f"{self.room.room_number} - {self.label}"
