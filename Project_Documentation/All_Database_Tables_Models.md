# Smart PG Management System - Django Database Models

This file contains the complete Django ORM models for the project, designed to support all core and advanced features. The models are structured into application-based modules for clarity and scalability.

---

## **1. `users` App Models**

Handles all user-related data, roles, profiles, and authentication logic.

```python
# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUser(AbstractUser):
    """
    Central user model for authentication and role management.
    Covers: Module 1 (User Roles & Auth)
    """
    class Roles(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', _('Super Admin (Owner)')
        MANAGER = 'MANAGER', _('Manager (Warden)')
        TENANT = 'TENANT', _('Tenant (Student)')
        PARENT = 'PARENT', _('Parent (Guardian)')
        STAFF = 'STAFF', _('Staff (Cook, Guard)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.TENANT)
    phone_number = models.CharField(max_length=15, unique=True, help_text="Used for login and notifications.")
    email = models.EmailField(unique=True, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # USP 11: Women Safety & SOS Button
    sos_contact_number = models.CharField(max_length=15, null=True, blank=True, help_text="Emergency contact for SOS alerts.")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class TenantProfile(models.Model):
    """
    Extended profile for tenants (students).
    Covers: USPs 1, 2, 6, 8, 10, 15
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'TENANT'})
    
    # USP 1: Parent Portal Access
    guardian = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards', limit_choices_to={'role': 'PARENT'})
    
    # USP 2: Aadhaar + Police Verification
    aadhaar_number = models.CharField(max_length=12, null=True, blank=True)
    police_verification_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUBMITTED', 'Submitted'), ('VERIFIED', 'Verified')], default='PENDING')
    
    # USP 10: Tenant Credit Score
    credit_score = models.IntegerField(default=700, help_text="Score for timely payments and good conduct.")
    
    # USP 6: AI Compatibility Matching
    lifestyle_attributes = models.JSONField(default=dict, blank=True, help_text="e.g., {'sleep_time': 'late', 'smoker': false}")
    
    # USP 15: Smart Mess Wallet
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Tenant Profile: {self.user.username}"

class StaffProfile(models.Model):
    """
    Extended profile for staff members (cook, guard, etc.).
    Covers: Advanced Feature 3 (Staff & Payroll)
    """
    class StaffRoles(models.TextChoices):
        COOK = 'COOK', _('Cook')
        GUARD = 'GUARD', _('Security Guard')
        CLEANER = 'CLEANER', _('Cleaner')
        OTHER = 'OTHER', _('Other')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'STAFF'})
    staff_role = models.CharField(max_length=20, choices=StaffRoles.choices)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salary per day for payroll calculation.")
    assigned_property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    joining_date = models.DateField()

    def __str__(self):
        return f"Staff Profile: {self.user.username}"
```

---

## **2. `properties` App Models**

Manages PG branches, rooms, beds, and all physical assets.

```python
# properties/models.py
from django.db import models
import uuid

class Property(models.Model):
    """
    Represents a single PG branch.
    Covers: Advanced Feature 1 (Multi-Property Management)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='owned_properties', limit_choices_to={'role': 'SUPERADMIN'})
    manager = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_properties', limit_choices_to={'role': 'MANAGER'})
    
    # USP 13: Hygiene Scorecard - Public Display
    current_hygiene_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, help_text="Current hygiene rating out of 5")
    
    # Multi-language support
    preferred_language = models.CharField(max_length=10, choices=[('EN', 'English'), ('HI', 'Hindi'), ('TE', 'Telugu')], default='EN')
    
    # Property metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    """
    Represents a room within a PG property.
    Covers: Module 2 (Property & Rooms)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(default=2, help_text="Number of beds in the room.")
    
    # USP 4: Dynamic Pricing Engine
    base_rent_per_bed = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Room amenities for better filtering
    has_ac = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_attached_bathroom = models.BooleanField(default=False)
    floor_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ('property', 'room_number')

    def __str__(self):
        return f"{self.property.name} - Room {self.room_number}"

class PricingRule(models.Model):
    """
    Dynamic pricing rules for seasonal or demand-based rent adjustments.
    Covers: USP 4 (Dynamic Pricing Engine)
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='pricing_rules')
    rule_name = models.CharField(max_length=100, help_text="e.g., Summer Surge")
    start_month = models.IntegerField(choices=[(i, i) for i in range(1, 13)], help_text="1=January, 12=December")
    end_month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, help_text="e.g., 1.10 for 10% increase")
    
    def __str__(self):
        return f"{self.rule_name} ({self.price_multiplier}x)"

class Bed(models.Model):
    """
    The smallest bookable unit in a room.
    Covers: USPs 3, 5
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_label = models.CharField(max_length=5, help_text="e.g., A, B, Upper, Lower")
    
    # USP 3: Live "Vacant Bed" Public Link
    is_occupied = models.BooleanField(default=False, db_index=True)
    
    # USP 5: Smart Electricity Billing (IoT)
    iot_meter_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        unique_together = ('room', 'bed_label')

    def __str__(self):
        return f"{self.room} - Bed {self.bed_label}"

class ElectricityReading(models.Model):
    """
    IoT meter readings for individual bed energy consumption.
    Covers: USP 5 (Smart Electricity Billing)
    """
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='electricity_readings')
    meter_id = models.CharField(max_length=50)
    reading_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [models.Index(fields=['meter_id', 'timestamp'])]

    def __str__(self):
        return f"{self.meter_id} - {self.reading_kwh} units"

class Asset(models.Model):
    """
    Manages physical assets like ACs, geysers, etc.
    Covers: Advanced Feature 4 (Asset & Inventory)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='assets')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    name = models.CharField(max_length=100) # e.g., "1.5 Ton AC"
    qr_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    purchase_date = models.DateField()
    last_service_date = models.DateField(null=True, blank=True)
    next_service_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.property.name}"

class AssetServiceLog(models.Model):
    """
    History of all services/repairs done on an asset.
    Covers: Advanced Feature 4 (Asset & Inventory) - 'Scan history'
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='service_logs')
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField(help_text="Details of repair or service")
    serviced_by = models.CharField(max_length=100, help_text="Vendor or Staff name")
    bill_photo = models.ImageField(upload_to='asset_bills/', null=True, blank=True)
    
    def __str__(self):
        return f"Service for {self.asset.name} on {self.service_date}"
```

---

## **3. `tenants` App Models**

Handles the entire tenant lifecycle from booking to exit.

```python
# tenants/models.py
from django.db import models
import uuid

class Booking(models.Model):
    """
    Manages a tenant's stay in a specific bed.
    Covers: Module 3 (Tenant Lifecycle), USPs 7, 8, 9
    """
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        NOTICE_PERIOD = 'NOTICE_PERIOD', 'On Notice Period'
        EXITED = 'EXITED', 'Exited'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='bookings', limit_choices_to={'role': 'TENANT'})
    bed = models.ForeignKey('properties.Bed', on_delete=models.PROTECT, related_name='bookings')
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    # USP 8: Zero-Deposit Option
    is_zero_deposit = models.BooleanField(default=False)
    fintech_partner_name = models.CharField(max_length=100, null=True, blank=True)
    fintech_loan_id = models.CharField(max_length=100, null=True, blank=True)
    
    # USP 9: Digital Notice Period & Auto Refund
    notice_given_date = models.DateField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_processed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.tenant.username} in {self.bed}"

class DigitalAgreement(models.Model):
    """
    Stores e-signed rental agreements.
    Covers: USP 7 (Digital Agreement)
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    agreement_file = models.FileField(upload_to='agreements/')
    is_signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Agreement for {self.booking}"
```

---

## **4. `finance` App Models**

Manages all financial transactions, invoices, expenses, and payroll.

```python
# finance/models.py
from django.db import models
import uuid

class Invoice(models.Model):
    """
    Monthly invoice for tenants.
    Covers: Module 4 (Finance)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('tenants.Booking', on_delete=models.PROTECT)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mess_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    electricity_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_paid = models.BooleanField(default=False, db_index=True)
    paid_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for {self.booking.tenant.username} - {self.issue_date.strftime('%B %Y')}"

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
    category = models.CharField(max_length=20, choices=Category.choices)
    is_credit = models.BooleanField(help_text="True if money is coming in, False if going out.")
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    payment_gateway_txn_id = models.CharField(max_length=100, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', help_text="Linked invoice if this txn pays a bill.")

    def __str__(self):
        return f"{self.get_category_display()} of {self.amount} for {self.user.username}"

class Expense(models.Model):
    """
    Logs all operational expenses for a property.
    Covers: Advanced Feature 2 (Expense Management)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    category = models.CharField(max_length=50) # e.g., Groceries, Maintenance, Utility Bill
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"Expense: {self.category} - {self.amount}"
```

---

## **5. `operations` App Models**

Handles day-to-day operations, safety, complaints, and notices.

```python
# operations/models.py
from django.db import models
import uuid

class Complaint(models.Model):
    """
    Tenant complaint management system.
    Covers: Module 5 (Operations & Safety)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint #{self.id} by {self.tenant.username}"

class EntryLog(models.Model):
    """
    Biometric/QR code entry and exit logs.
    Covers: USP 12 (Biometric/QR Entry + Night Alert)
    """
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')])
    entry_method = models.CharField(max_length=20, choices=[('BIOMETRIC', 'Biometric'), ('QR', 'QR Code'), ('MANUAL', 'Manual')], default='MANUAL')
    is_late_entry = models.BooleanField(default=False)
    parent_alert_sent = models.BooleanField(default=False)

class Notice(models.Model):
    """
    Digital notice board for broadcasting messages.
    Covers: Advanced Feature 7 (Digital Notice Board)
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ChatLog(models.Model):
    """
    Logs interactions between students and the AI Chatbot.
    Covers: USP 14 (AI Chatbot)
    """
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    message = models.TextField(help_text="User's question")
    bot_response = models.TextField(help_text="AI's answer")
    intent = models.CharField(max_length=50, null=True, blank=True, help_text="Detected intent e.g., 'rent_query'")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.tenant.username} at {self.timestamp}"
```

---

## **6. `mess` App Models**

Manages the smart mess, menu, and daily meal selections.

```python
# mess/models.py
from django.db import models
import uuid

class MessMenu(models.Model):
    """
    Weekly or daily menu for the mess.
    Covers: Module 6 (Smart Mess)
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    date = models.DateField()
    breakfast = models.CharField(max_length=255, null=True, blank=True)
    lunch = models.CharField(max_length=255, null=True, blank=True)
    dinner = models.CharField(max_length=255, null=True, blank=True)
    
    price_breakfast = models.DecimalField(max_digits=6, decimal_places=2)
    price_lunch = models.DecimalField(max_digits=6, decimal_places=2)
    price_dinner = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('property', 'date')

    def __str__(self):
        return f"Menu for {self.date} at {self.property.name}"

class DailyMealSelection(models.Model):
    """
    Tenant's daily choice for meals, enabling the pay-per-day wallet system.
    Covers: USP 15 (Pay-per-Day Mess Wallet)
    """
    class MealStatus(models.TextChoices):
        EATING = 'EATING', 'Eating'
        SKIPPING = 'SKIPPING', 'Skipping'

    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    menu = models.ForeignKey(MessMenu, on_delete=models.CASCADE)
    
    breakfast_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING)
    lunch_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING)
    dinner_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING)
    
    is_billed = models.BooleanField(default=False, help_text="True once the cost is debited from wallet.")

    class Meta:
        unique_together = ('tenant', 'menu')

    def __str__(self):
        return f"Meal selection for {self.tenant.username} on {self.menu.date}"
```

---

## **7. `crm` App Models**

Manages leads and enquiries for new tenants.

```python
# crm/models.py
from django.db import models
import uuid

class Lead(models.Model):
    """
    Tracks enquiries from potential tenants.
    Covers: Advanced Feature 5 (CRM & Lead Management)
    """
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        VISITED = 'VISITED', 'Visited'
        CONVERTED = 'CONVERTED', 'Converted'
        LOST = 'LOST', 'Lost'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    converted_tenant = models.OneToOneField('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_record', help_text="Linked tenant profile if converted.")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead: {self.full_name} for {self.property.name}"
```

---

## **8. `notifications` App Models**

Handles all notification logs and FCM tokens.

```python
# notifications/models.py
from django.db import models
import uuid

class NotificationLog(models.Model):
    """
    Logs all notifications sent to users.
    Covers: Technical Feature 1 (Notification System)
    """
    class NotificationType(models.TextChoices):
        SMS = 'SMS', 'SMS'
        EMAIL = 'EMAIL', 'Email'
        PUSH = 'PUSH', 'Push Notification'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'

    class NotificationCategory(models.TextChoices):
        RENT_REMINDER = 'RENT_REMINDER', 'Rent Reminder'
        PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Success'
        COMPLAINT_UPDATE = 'COMPLAINT_UPDATE', 'Complaint Update'
        NIGHT_ALERT = 'NIGHT_ALERT', 'Night Entry Alert'
        SOS_ALERT = 'SOS_ALERT', 'SOS Alert'
        NOTICE = 'NOTICE', 'Notice Board'
        GENERAL = 'GENERAL', 'General'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    category = models.CharField(max_length=30, choices=NotificationCategory.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.user.username}"

class FCMToken(models.Model):
    """
    Stores Firebase Cloud Messaging tokens for push notifications.
    Covers: Technical Feature 1 (Notification System)
    """
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web')])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FCM Token for {self.user.username}"
```

---

## **9. `visitors` App Models**

Manages visitor entry and approval system.

```python
# visitors/models.py
from django.db import models
import uuid

class VisitorRequest(models.Model):
    """
    Tracks visitor entry requests and approvals.
    Covers: Advanced Feature 6 (Visitor Management)
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CHECKED_OUT = 'CHECKED_OUT', 'Checked Out'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='visitor_requests', limit_choices_to={'role': 'TENANT'})
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=15)
    visitor_photo = models.ImageField(upload_to='visitors/', null=True, blank=True)
    purpose = models.CharField(max_length=255)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    guard = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_visitors', limit_choices_to={'role': 'STAFF'})

    def __str__(self):
        return f"Visitor {self.visitor_name} for {self.tenant.username}"
```

---

## **10. `inventory` App Models**

Manages kitchen stock and inventory tracking.

```python
# inventory/models.py
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
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, help_text="e.g., Groceries, Vegetables, Dairy")
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)
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
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.item_name}"
```

---

## **11. `payroll` App Models**

Manages staff attendance and salary payments.

```python
# payroll/models.py
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
    date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
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
    staff = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='salary_payments', limit_choices_to={'role': 'STAFF'})
    property = models.ForeignKey('properties.Property', on_delete=models.PROTECT)
    month = models.DateField(help_text="First day of the salary month")
    days_worked = models.DecimalField(max_digits=5, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=20, choices=[('CASH', 'Cash'), ('BANK', 'Bank Transfer'), ('UPI', 'UPI')])
    transaction_reference = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('staff', 'month')

    def __str__(self):
        return f"Salary for {self.staff.username} - {self.month.strftime('%B %Y')}"
```

---

## **12. `hygiene` App Models**

Tracks hygiene inspections and ratings.

```python
# hygiene/models.py
from django.db import models
import uuid

class HygieneInspection(models.Model):
    """
    Weekly hygiene inspection records.
    Covers: USP 13 (Hygiene Scorecard)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='hygiene_inspections')
    inspection_date = models.DateField()
    inspector = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role__in': ['MANAGER', 'SUPERADMIN']})
    
    cleanliness_score = models.IntegerField(help_text="Score out of 10")
    kitchen_score = models.IntegerField(help_text="Score out of 10")
    bathroom_score = models.IntegerField(help_text="Score out of 10")
    common_area_score = models.IntegerField(help_text="Score out of 10")
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, help_text="Average rating out of 5")
    photos = models.JSONField(default=list, help_text="List of photo URLs")
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Hygiene Inspection - {self.property.name} on {self.inspection_date}"
```

---

## **13. `feedback` App Models**

Collects ratings and feedback from tenants.

```python
# feedback/models.py
from django.db import models
import uuid

class ComplaintFeedback(models.Model):
    """
    Tenant feedback on resolved complaints.
    Covers: Technical Feature 9 (Feedback & Rating Loop)
    """
    complaint = models.OneToOneField('operations.Complaint', on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(help_text="Rating from 1 to 5")
    feedback_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Complaint #{self.complaint.id}"

class MessFeedback(models.Model):
    """
    Daily feedback on mess food quality.
    Covers: Technical Feature 9 (Feedback & Rating Loop)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    menu = models.ForeignKey('mess.MessMenu', on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=[('BREAKFAST', 'Breakfast'), ('LUNCH', 'Lunch'), ('DINNER', 'Dinner')])
    rating = models.IntegerField(help_text="Rating from 1 to 5")
    feedback_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mess Feedback by {self.tenant.username} on {self.menu.date}"
```

---

## **14. `audit` App Models**

Tracks all system activities for security and fraud detection.

```python
# audit/models.py
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
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    model_name = models.CharField(max_length=100, help_text="Name of the model affected")
    object_id = models.CharField(max_length=100, help_text="ID of the affected object")
    changes = models.JSONField(default=dict, help_text="Before and after values")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.get_action_type_display()} on {self.model_name}"
```

---

## **15. `alumni` App Models**

Manages alumni network and job referrals.

```python
# alumni/models.py
from django.db import models
import uuid

class AlumniProfile(models.Model):
    """
    Extended profile for ex-tenants (alumni).
    Covers: Advanced Feature 9 (Alumni Network)
    """
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, primary_key=True)
    current_company = models.CharField(max_length=100, null=True, blank=True)
    current_position = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    is_open_to_referrals = models.BooleanField(default=False)
    exit_date = models.DateField(help_text="Date when tenant left the PG")
    properties_stayed = models.ManyToManyField('properties.Property', related_name='alumni')

    def __str__(self):
        return f"Alumni: {self.user.username}"

class JobReferral(models.Model):
    """
    Job referral requests between alumni and current tenants.
    Covers: Advanced Feature 9 (Alumni Network)
    """
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='referral_requests')
    alumni = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='referrals_given')
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Referral request from {self.requester.username} to {self.alumni.username}"
```

---

## **16. `saas` App Models**

Manages subscription plans for multi-tenant SaaS model.

```python
# saas/models.py
from django.db import models
import uuid

class SubscriptionPlan(models.Model):
    """
    Defines different subscription tiers for PG owners.
    Covers: Technical Feature 8 (The SaaS Angle)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, help_text="e.g., Basic, Gold, Platinum")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    max_properties = models.IntegerField(help_text="Maximum number of PG branches allowed")
    max_rooms = models.IntegerField(help_text="Maximum total rooms across all properties")
    features = models.JSONField(default=dict, help_text="Feature flags: {'crm': true, 'alumni': false}")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PropertySubscription(models.Model):
    """
    Tracks subscription status for each property owner.
    Covers: Technical Feature 8 (The SaaS Angle)
    """
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'
        TRIAL = 'TRIAL', 'Trial'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'SUPERADMIN'})
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIAL)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner.username} - {self.plan.name}"

class AppVersion(models.Model):
    """
    Manages app versions for forced updates.
    Covers: Technical Feature 5 (Version Control & App Updates)
    """
    platform = models.CharField(max_length=10, choices=[('ANDROID', 'Android'), ('IOS', 'iOS')])
    version_code = models.IntegerField(help_text="e.g., 102")
    version_name = models.CharField(max_length=20, help_text="e.g., 1.0.2")
    is_mandatory = models.BooleanField(default=False, help_text="Force update required?")
    release_date = models.DateField()
    
    def __str__(self):
        return f"{self.platform} - {self.version_name}"
```

---

## **17. `reports` App Models**

Stores generated reports for analytics.

```python
# reports/models.py
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
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='reports/')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
```

---

---

## **Summary**

### **Total Apps: 18**
1. users
2. properties
3. tenants
4. finance
5. operations
6. mess
7. crm
8. notifications
9. visitors
10. inventory
11. payroll
12. hygiene
13. feedback
14. audit
15. alumni
16. saas
17. reports
18. (core Django apps)

### **Total Models: 35+**

All models are now complete with integrated fields supporting:
- ✅ All 6 Core Modules
- ✅ All 15 USP Features
- ✅ All 9 Advanced Features
- ✅ All 9 Technical Features

**Database schema is production-ready for Phase 1 development!**