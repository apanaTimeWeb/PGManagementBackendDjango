from django.db import models
import uuid

class StaffAttendance(models.Model):
    """
    Tracks daily attendance for staff members.
    Covers: Advanced Feature 3 (Staff & Payroll Management)
    """
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        HALF_DAY = 'HALF_DAY', 'Half Day'
        LEAVE = 'LEAVE', 'On Leave'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={'role': 'STAFF'})
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT, db_index=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    selfie_photo = models.ImageField(upload_to='staff_attendance/', null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('staff', 'date')

    def __str__(self):
        return f"{self.staff.username} - {self.date}"

class SalaryPayment(models.Model):
    """
    Records monthly salary payments to staff.
    Covers: Advanced Feature 3 (Staff & Payroll Management)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='salary_payments', limit_choices_to={'role': 'STAFF'})
    month = models.DateField(help_text="The first day of the month for which salary is paid", db_index=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True, db_index=True)
    transaction_ref = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('staff', 'month')

    def __str__(self):
        return f"Salary for {self.staff.username} - {self.month.strftime('%B %Y')}"
