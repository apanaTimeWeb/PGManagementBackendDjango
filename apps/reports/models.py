from django.db import models
import uuid

class GeneratedReport(models.Model):
    """
    Stores generated Excel/PDF reports for download.
    Covers: Advanced Feature 8 (Reporting & Analytics Module)
    """
    class ReportType(models.TextChoices):
        MONTHLY_RENT = 'MONTHLY_RENT', 'Monthly Rent Report'
        EXPENSE = 'EXPENSE', 'Expense Report'
        GST = 'GST', 'GST Report'
        OCCUPANCY = 'OCCUPANCY', 'Occupancy Trends'
        STAFF_PAYROLL = 'STAFF_PAYROLL', 'Staff Payroll'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=30, choices=ReportType.choices, db_index=True)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='reports/')
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
