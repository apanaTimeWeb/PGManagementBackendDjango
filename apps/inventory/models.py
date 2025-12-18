from django.db import models
import uuid

class InventoryItem(models.Model):
    """
    Tracks kitchen stock and supplies.
    Covers: Advanced Feature 4 (Asset & Inventory Management)
    """
    class Unit(models.TextChoices):
        KG = 'KG', 'Kilogram'
        LITER = 'LITER', 'Liter'
        PIECE = 'PIECE', 'Piece'
        PACKET = 'PACKET', 'Packet'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=50, help_text="e.g., Groceries, Vegetables, Dairy", db_index=True)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    unit = models.CharField(max_length=20, choices=Unit.choices)
    minimum_threshold = models.DecimalField(max_digits=10, decimal_places=2, help_text="Alert when stock falls below this")
    last_restocked_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} - {self.current_quantity} {self.unit}"

class InventoryTransaction(models.Model):
    """
    Logs all inventory movements (purchase, consumption).
    """
    class TransactionType(models.TextChoices):
        PURCHASE = 'PURCHASE', 'Purchase'
        CONSUMPTION = 'CONSUMPTION', 'Consumption'
        WASTAGE = 'WASTAGE', 'Wastage'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, db_index=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, db_index=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.item_name}"
