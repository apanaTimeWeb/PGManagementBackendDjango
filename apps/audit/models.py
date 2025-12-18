from django.db import models
import uuid

class AuditLog(models.Model):
    """
    Comprehensive audit trail for all critical actions.
    Covers: Technical Feature 7 (Audit Logs)
    """
    class ActionType(models.TextChoices):
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'
        LOGIN = 'LOGIN', 'Login'
        LOGOUT = 'LOGOUT', 'Logout'
        PAYMENT = 'PAYMENT', 'Payment'
        REFUND = 'REFUND', 'Refund'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ActionType.choices, db_index=True)
    model_name = models.CharField(max_length=100, help_text="Name of the model affected", db_index=True)
    object_id = models.CharField(max_length=100, help_text="ID of the affected object", db_index=True)
    changes = models.JSONField(default=dict, help_text="Before and after values")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.get_action_type_display()} on {self.model_name}"
