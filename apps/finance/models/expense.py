from django.db import models
import uuid

class Expense(models.Model):
    """
    Logs all operational expenses for a property.
    Covers: Advanced Feature 2 (Expense Management)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, db_index=True) # e.g., Groceries, Maintenance, Utility Bill
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(db_index=True)
    description = models.TextField()
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"Expense: {self.category} - {self.amount}"
