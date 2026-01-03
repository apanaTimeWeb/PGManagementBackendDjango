from django.db import models
import uuid
from .custom_user import CustomUser
from .tenant_profile import TenantProfile

class ParentStudentMapping(models.Model):
    """
    Explicit mapping between Parent and Student Users.
    Ref: Table ParentStudentMapping in DBML
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='children_mappings', limit_choices_to={'role': 'PARENT'})
    student_tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE, related_name='parent_mappings')
    relationship = models.CharField(max_length=50, choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('GUARDIAN', 'Guardian')])
    has_access = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent_user', 'student_tenant')
