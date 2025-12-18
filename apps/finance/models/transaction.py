from django.db import models
import uuid
from .invoice import Invoice

class Transaction(models.Model):
    """
    Logs all financial movements: rent, wallet, refunds, etc.
    """
    class Category(models.TextChoices):
        RENT = 'RENT', 'Rent Payment'
        WALLET_RECHARGE = 'WALLET_RECHARGE', 'Wallet Recharge'
        MESS_DEBIT = 'MESS_DEBIT', 'Mess Debit'
        REFUND = 'REFUND', 'Security Deposit Refund'
        EXPENSE = 'EXPENSE', 'PG Expense'
        SALARY = 'SALARY', 'Staff Salary'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, help_text="User involved in the transaction.")
    property = models.ForeignKey('properties.Property', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    is_credit = models.BooleanField(help_text="True if money is coming in, False if going out.", db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.CharField(max_length=255)
    payment_gateway_txn_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', help_text="Linked invoice if this txn pays a bill.")

    def __str__(self):
        return f"{self.get_category_display()} of {self.amount} for {self.user.username}"
