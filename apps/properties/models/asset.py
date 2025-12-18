from django.db import models
import uuid

class Asset(models.Model):
    """
    Manages physical assets like ACs, geysers, etc.
    Covers: Advanced Feature 4 (Asset & Inventory)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='assets')
    room = models.ForeignKey('properties.Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    name = models.CharField(max_length=100) # e.g., "1.5 Ton AC"
    qr_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    purchase_date = models.DateField()
    last_service_date = models.DateField(null=True, blank=True)
    next_service_due_date = models.DateField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.name}"

class AssetServiceLog(models.Model):
    """
    History of all services/repairs done on an asset.
    Covers: Advanced Feature 4 (Asset & Inventory) - 'Scan history'
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='service_logs')
    service_date = models.DateField(db_index=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField(help_text="Details of repair or service")
    serviced_by = models.CharField(max_length=100, help_text="Vendor or Staff name")
    bill_photo = models.ImageField(upload_to='asset_bills/', null=True, blank=True)
    
    def __str__(self):
        return f"Service for {self.asset.name} on {self.service_date}"
