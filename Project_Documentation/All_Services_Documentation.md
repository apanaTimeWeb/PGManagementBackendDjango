# 🏨 Smart PG Management System - Service Documentation (Modular Monolith)

## 1. INTRODUCTION

Ye documentation **Smart PG Management System** ke liye hai, jisme **6 independent Django apps** ka detailed description diya gaya hai. Ye apps modular monolith architecture follow karti hain with **12 Django models** across different apps.

### 1.1 Project Overview
- **Architecture Type**: Modular Monolith Architecture (Django)
- **Total Apps**: 6 (+ 1 Core Settings)
- **Total Models**: 12 database models
- **Communication**: Direct Python Imports (Synchronous)
- **Database**: PostgreSQL/SQLite (single database)
- **Authentication**: JWT-based
- **Language**: Python 3.10+ with Django 4.2+

### 1.2 Technology Stack
- **Backend Framework**: Django REST Framework
- **ORM**: Django ORM
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Validation**: Django REST Framework serializers
- **File Storage**: Django FileField/ImageField
- **Task Queue**: Celery (for background tasks)
- **Caching**: Redis (optional)

### 1.3 Documentation Purpose
Ye documentation developers ke liye hai jo:
- Django modular monolith ko understand karna chahte hain
- Individual apps ko develop/maintain karenge
- Inter-app communication implement karenge
- API endpoints ko integrate karenge
- System architecture ko samajhna chahte hain

### 1.4 Kyun Modular Monolith Best Hai?
Beginners ke liye Microservices banana mushkil hota hai (Network issues, Docker, Kubernetes).
**Modular Monolith** mein:
1. **Speed**: Ek app dusre app ko millisecond mein call karta hai
2. **Simplicity**: Sab kuch ek jagah hai, debug karna aasaan hai
3. **Scalability**: Future mein agar zaroorat padi, toh kisi bhi app ko alag server par daal sakte hain
4. **Database Consistency**: Single database, no distributed transaction issues

---

## MODULAR MONOLITH ARCHITECTURE OVERVIEW

### App Distribution (6 Apps, 12 Models)
1. **User Management App** (`apps/users`): CustomUser, TenantProfile (2 models)
2. **Property & Inventory App** (`apps/inventory`): Room, Bed (2 models)
3. **Booking Management App** (`apps/bookings`): Booking (1 model)
4. **Finance Management App** (`apps/finance`): Invoice, WalletTransaction (2 models)
5. **Operations & Safety App** (`apps/operations`): Complaint, EntryLog, HygieneRating (3 models)
6. **Smart Mess App** (`apps/mess`): MessMenu, DailyMealSelection (2 models)

### Django Project Structure
```
smart_pg_backend/
├── core/                    # Django settings, global utilities
│   ├── settings/
│   ├── urls.py             # Main URL routing
│   └── wsgi.py
├── apps/
│   ├── users/              # App 1: Authentication & User Management
│   │   ├── models.py       # CustomUser, TenantProfile
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── urls.py         # App URLs
│   │   └── services.py     # Business logic
│   ├── inventory/          # App 2: Rooms & Beds
│   ├── bookings/           # App 3: Booking Lifecycle
│   ├── finance/            # App 4: Money & Wallet
│   ├── operations/         # App 5: Complaints & Safety
│   └── mess/               # App 6: Smart Food System
├── requirements.txt
└── manage.py
```

### URL Configuration
```python
# core/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/bookings/', include('apps.bookings.urls')),
    path('api/v1/finance/', include('apps.finance.urls')),
    path('api/v1/operations/', include('apps.operations.urls')),
    path('api/v1/mess/', include('apps.mess.urls')),
]
```

---

## APP 1: USER MANAGEMENT SERVICE (`apps/users`)

### Models: CustomUser, TenantProfile
User management mein user registration, login, password reset, profile update, aur parent portal ke features shamil hain.

#### 1.1 User Registration & Authentication
**Endpoint**: POST /api/v1/auth/register/  
**Description**: Naye users (Admin, Manager, Tenant, Parent) ko register karne ke liye.  

**Request Body**:
```json
{
  "username": "rahul_sharma",
  "email": "rahul@example.com",
  "phone_number": "+919876543210",
  "password": "Pass@123",
  "role": "TENANT"
}
```

**Database Interaction**:
- **CustomUser Table**: Naya record create with hashed password
- **TenantProfile Table**: Agar role = 'TENANT', toh automatic profile create

**Business Logic**:
```python
# apps/users/services.py
from django.contrib.auth.hashers import make_password
from .models import CustomUser, TenantProfile

def register_user(validated_data):
    # Create user with hashed password
    user = CustomUser.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        phone_number=validated_data['phone_number'],
        password=make_password(validated_data['password']),
        role=validated_data['role']
    )
    
    # Auto-create TenantProfile for students
    if user.role == 'TENANT':
        TenantProfile.objects.create(
            user=user,
            police_verification_status='PENDING',
            pg_credit_score=700,
            wallet_balance=0.00
        )
    
    return user
```

**Response**:
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "rahul_sharma",
    "role": "TENANT"
  }
}
```

#### 1.2 User Login
**Endpoint**: POST /api/v1/auth/login/  
**Description**: Users ko authenticate karke JWT token deta hai.  

**Request Body**:
```json
{
  "username": "rahul_sharma",
  "password": "Pass@123"
}
```

**Database Interaction**:
- **CustomUser Table**: Username se record fetch, password verify
- JWT token generate with `user_id`, `role`

**Response**:
```json
{
  "success": true,
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "rahul_sharma",
    "role": "TENANT"
  }
}
```

#### 1.3 Parent Portal Access (USP 1)
**Endpoint**: GET /api/v1/auth/parent/my-wards/  
**Description**: Parent ko unke bachon ki details dikhata hai.  

**Database Interaction**:
- **TenantProfile Table**: guardian_user = current_user ke records fetch

**Business Logic**:
```python
# apps/users/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_wards(request):
    if request.user.role != 'PARENT':
        return Response({'error': 'Only parents can access this'}, status=403)
    
    wards = TenantProfile.objects.filter(guardian_user=request.user)
    serializer = TenantProfileSerializer(wards, many=True)
    return Response({'success': True, 'wards': serializer.data})
```

**Response**:
```json
{
  "success": true,
  "wards": [
    {
      "user": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "rahul_sharma",
        "phone_number": "+919876543210"
      },
      "pg_credit_score": 750,
      "wallet_balance": "2500.00",
      "police_verification_status": "VERIFIED"
    }
  ]
}
```

#### 1.4 SOS Alert System (USP 11)
**Endpoint**: POST /api/v1/auth/sos/trigger/  
**Description**: Emergency alert system for student safety.  

**Request Body**:
```json
{
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090
  },
  "message": "Emergency help needed"
}
```

**Business Logic**:
```python
# apps/users/services.py
from django.core.mail import send_mail
import requests

def trigger_sos_alert(user, location, message):
    # Get guardian contact
    tenant_profile = user.tenant_profile
    guardian = tenant_profile.guardian_user
    
    # Get manager contact
    manager = CustomUser.objects.filter(role='MANAGER').first()
    
    # Send SMS to both
    sms_message = f"EMERGENCY: {user.username} needs help at {location['latitude']}, {location['longitude']}. Message: {message}"
    
    # Send to guardian
    if guardian and guardian.phone_number:
        send_sms(guardian.phone_number, sms_message)
    
    # Send to manager
    if manager and manager.phone_number:
        send_sms(manager.phone_number, sms_message)
    
    return True

def send_sms(phone_number, message):
    # Integration with SMS gateway (Twilio/Fast2SMS)
    # Implementation depends on chosen SMS service
    pass
```

#### 1.5 Profile Management
**Update Profile**  
**Endpoint**: PUT /api/v1/auth/profile/  
**Description**: User profile update karta hai.  

**Aadhaar Upload (USP 2)**  
**Endpoint**: POST /api/v1/auth/aadhaar/upload/  
**Description**: Aadhaar card upload aur police verification trigger.  

**Internal APIs for Other Apps**:
```python
# For other apps to get user details
GET /api/v1/auth/internal/users/{user_id}/
GET /api/v1/auth/internal/tenant-profile/{user_id}/
```

---

## APP 2: PROPERTY & INVENTORY SERVICE (`apps/inventory`)

### Models: Room, Bed
Property management mein rooms, beds, aur inventory tracking ke features shamil hain.

#### 2.1 Room Management
**List Rooms**  
**Endpoint**: GET /api/v1/inventory/rooms/  
**Description**: Available rooms ki list with filters.  

**Query Parameters**:
```
?floor=2&has_ac=true&capacity=2&available=true
```

**Database Interaction**:
- **Room Table**: Filters ke according rooms fetch
- **Bed Table**: Room ke beds count aur availability check

**Response**:
```json
{
  "success": true,
  "rooms": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "room_number": "204-B",
      "floor": 2,
      "capacity": 2,
      "has_ac": true,
      "has_balcony": false,
      "base_rent": "8000.00",
      "current_seasonal_rent": "9000.00",
      "available_beds": 1,
      "total_beds": 2
    }
  ]
}
```

#### 2.2 Live Vacant Bed Link (USP 3)
**Endpoint**: GET /api/v1/inventory/public/bed/{public_uid}/  
**Description**: Public link se bed details without login.  

**URL Example**: `https://smartpg.com/api/v1/inventory/public/bed/550e8400-e29b-41d4-a716-446655440020/`

**Database Interaction**:
- **Bed Table**: public_uid se bed search
- **Room Table**: Bed ki room details fetch

**Business Logic**:
```python
# apps/inventory/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_bed_by_public_link(request, public_uid):
    try:
        bed = Bed.objects.select_related('room').get(public_uid=public_uid)
        
        if bed.is_occupied:
            return Response({
                'success': False,
                'message': 'Sorry, this bed is already booked'
            }, status=400)
        
        return Response({
            'success': True,
            'bed': {
                'id': bed.id,
                'bed_label': bed.bed_label,
                'room': {
                    'room_number': bed.room.room_number,
                    'floor': bed.room.floor,
                    'has_ac': bed.room.has_ac,
                    'current_rent': bed.room.current_seasonal_rent
                }
            }
        })
    except Bed.DoesNotExist:
        return Response({'error': 'Bed not found'}, status=404)
```

**Response**:
```json
{
  "success": true,
  "bed": {
    "id": "550e8400-e29b-41d4-a716-446655440020",
    "bed_label": "A",
    "room": {
      "room_number": "204-B",
      "floor": 2,
      "has_ac": true,
      "current_rent": "9000.00"
    }
  }
}
```

#### 2.3 Smart Electricity Meter (USP 5)
**Endpoint**: POST /api/v1/inventory/iot/meter-reading/  
**Description**: IoT devices se electricity readings receive karta hai.  

**Request Body**:
```json
{
  "meter_id": "IOT-METER-X99",
  "current_reading": 1250.75,
  "timestamp": "2025-11-20T10:30:00Z"
}
```

**Database Interaction**:
- **Bed Table**: meter_id se bed find karo
- Update `last_meter_reading` aur `current_meter_reading`

**Business Logic**:
```python
# apps/inventory/services.py
from django.utils import timezone

def update_meter_reading(meter_id, current_reading, timestamp):
    try:
        bed = Bed.objects.get(iot_meter_id=meter_id)
        
        # Update readings
        bed.last_meter_reading = bed.current_meter_reading
        bed.current_meter_reading = current_reading
        bed.save()
        
        # Calculate usage for billing
        usage = current_reading - bed.last_meter_reading
        
        # Trigger billing calculation if needed
        if usage > 0:
            from apps.finance.services import calculate_electricity_bill
            calculate_electricity_bill(bed, usage)
        
        return True
    except Bed.DoesNotExist:
        return False
```

#### 2.4 Dynamic Pricing Engine (USP 4)
**Endpoint**: PUT /api/v1/inventory/rooms/{room_id}/pricing/  
**Description**: Seasonal pricing update (Admin only).  

**Request Body**:
```json
{
  "season": "PEAK",
  "multiplier": 1.2
}
```

**Business Logic**:
```python
# apps/inventory/services.py
def update_seasonal_pricing(room_id, season, multiplier):
    room = Room.objects.get(id=room_id)
    
    if season == 'PEAK':  # June-July
        room.current_seasonal_rent = room.base_rent * multiplier
    elif season == 'LOW':  # Winter months
        room.current_seasonal_rent = room.base_rent * 0.8
    else:  # Normal season
        room.current_seasonal_rent = room.base_rent
    
    room.save()
    return room
```

#### 2.5 Internal APIs for Other Apps
```python
# For booking app to check availability
GET /api/v1/inventory/internal/bed/{bed_id}/availability/
PUT /api/v1/inventory/internal/bed/{bed_id}/occupy/
PUT /api/v1/inventory/internal/bed/{bed_id}/vacate/

# For finance app to get meter readings
GET /api/v1/inventory/internal/bed/{bed_id}/meter-reading/
```

---

## APP 3: BOOKING MANAGEMENT SERVICE (`apps/bookings`)

### Models: Booking
Booking management mein bed booking, agreements, aur tenant lifecycle ke features shamil hain.

#### 3.1 Create Booking
**Endpoint**: POST /api/v1/bookings/create/  
**Description**: Naya booking create karta hai with multiple payment options.  

**Request Body**:
```json
{
  "bed_id": "550e8400-e29b-41d4-a716-446655440020",
  "start_date": "2025-12-01",
  "payment_mode": "FINTECH_LOAN",
  "loan_provider_name": "PayLater Finance"
}
```

**Inter-App Communication**:
```python
# apps/bookings/services.py
from apps.inventory.models import Bed
from apps.finance.models import WalletTransaction

def create_booking(user, validated_data):
    # Check bed availability
    bed = Bed.objects.get(id=validated_data['bed_id'])
    if bed.is_occupied:
        raise ValidationError("Bed is already occupied")
    
    # Create booking
    booking = Booking.objects.create(
        tenant=user,
        bed=bed,
        start_date=validated_data['start_date'],
        payment_mode=validated_data['payment_mode'],
        loan_provider_name=validated_data.get('loan_provider_name'),
        status='ACTIVE'
    )
    
    # Mark bed as occupied
    bed.is_occupied = True
    bed.save()
    
    # Handle payment based on mode
    if validated_data['payment_mode'] == 'FINTECH_LOAN':
        # Zero deposit logic
        booking.status = 'WAITING_FOR_LOAN_APPROVAL'
        booking.save()
    elif validated_data['payment_mode'] == 'ONLINE':
        # Process deposit payment
        from apps.finance.services import process_deposit_payment
        process_deposit_payment(booking, bed.room.current_seasonal_rent)
    
    return booking
```

**Response**:
```json
{
  "success": true,
  "booking": {
    "id": "550e8400-e29b-41d4-a716-446655440030",
    "bed": {
      "room_number": "204-B",
      "bed_label": "A"
    },
    "start_date": "2025-12-01",
    "status": "ACTIVE",
    "payment_mode": "FINTECH_LOAN"
  }
}
```

#### 3.2 Digital Agreement (USP 7)
**Upload Agreement**  
**Endpoint**: POST /api/v1/bookings/{booking_id}/agreement/upload/  
**Description**: Digital agreement upload aur eSign.  

**Request**: Multipart form with PDF file

**Sign Agreement**  
**Endpoint**: POST /api/v1/bookings/{booking_id}/agreement/sign/  
**Description**: Digital signature capture.  

**Business Logic**:
```python
# apps/bookings/services.py
def sign_agreement(booking_id, signature_data):
    booking = Booking.objects.get(id=booking_id)
    
    # Process digital signature
    booking.is_signed_digitally = True
    booking.save()
    
    # Generate signed PDF (integrate with eSign service)
    # Store final signed document
    
    return booking
```

#### 3.3 Digital Notice Period & Auto Refund (USP 9)
**Request Exit**  
**Endpoint**: POST /api/v1/bookings/{booking_id}/request-exit/  
**Description**: Student exit request with automatic refund calculation.  

**Request Body**:
```json
{
  "exit_reason": "Course completed",
  "preferred_exit_date": "2025-12-31"
}
```

**Business Logic**:
```python
# apps/bookings/services.py
from datetime import date, timedelta

def request_exit(booking_id, exit_reason):
    booking = Booking.objects.get(id=booking_id)
    
    # Set notice date
    booking.notice_given_date = date.today()
    booking.status = 'NOTICE'
    
    # Calculate exit date (30 days notice)
    booking.end_date = date.today() + timedelta(days=30)
    booking.save()
    
    # Trigger final bill calculation
    from apps.finance.services import generate_final_bill
    final_bill = generate_final_bill(booking)
    
    # Calculate refund amount
    refund_amount = calculate_refund(booking)
    
    return {
        'booking': booking,
        'final_bill': final_bill,
        'refund_amount': refund_amount
    }

def calculate_refund(booking):
    # Calculate unused rent, deposit refund, etc.
    # Complex business logic for refund calculation
    pass
```

#### 3.4 Get User Bookings
**Endpoint**: GET /api/v1/bookings/my-bookings/  
**Description**: Current user ke sabhi bookings.  

**Response**:
```json
{
  "success": true,
  "bookings": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440030",
      "bed": {
        "room_number": "204-B",
        "bed_label": "A"
      },
      "start_date": "2025-12-01",
      "end_date": null,
      "status": "ACTIVE",
      "rent_amount": "9000.00"
    }
  ]
}
```

#### 3.5 Internal APIs for Other Apps
```python
# For finance app to get booking details
GET /api/v1/bookings/internal/user/{user_id}/active-booking/
GET /api/v1/bookings/internal/booking/{booking_id}/

# For operations app to verify tenant
GET /api/v1/bookings/internal/verify-tenant/{user_id}/{bed_id}/
```

---

## APP 4: FINANCE MANAGEMENT SERVICE (`apps/finance`)

### Models: Invoice, WalletTransaction
Finance management mein invoicing, payments, wallet, aur credit score ke features shamil hain.

#### 4.1 Auto Invoice Generation
**Trigger**: Monthly cron job (1st of every month)  
**Description**: Sabhi active bookings ke liye automatic invoice generate karta hai.  

**Business Logic**:
```python
# apps/finance/services.py
from django.utils import timezone
from apps.bookings.models import Booking
from apps.inventory.models import Bed

def generate_monthly_invoices():
    current_month = timezone.now().date().replace(day=1)
    active_bookings = Booking.objects.filter(status='ACTIVE')
    
    for booking in active_bookings:
        # Calculate rent
        rent_amount = booking.bed.room.current_seasonal_rent
        
        # Calculate electricity
        bed = booking.bed
        electricity_units = bed.current_meter_reading - bed.last_meter_reading
        electricity_amount = electricity_units * 8.0  # ₹8 per unit
        
        # Calculate mess total
        from apps.mess.services import get_monthly_mess_total
        mess_total = get_monthly_mess_total(booking.tenant, current_month)
        
        # Create invoice
        invoice = Invoice.objects.create(
            booking=booking,
            month=current_month,
            rent_amount=rent_amount,
            electricity_usage_units=electricity_units,
            electricity_amount=electricity_amount,
            mess_total=mess_total,
            total_due=rent_amount + electricity_amount + mess_total
        )
        
        # Send notification
        send_invoice_notification(booking.tenant, invoice)
```

#### 4.2 Wallet Management (USP 15 Integration)
**Get Wallet Balance**  
**Endpoint**: GET /api/v1/finance/wallet/balance/  
**Description**: Current user ka wallet balance.  

**Response**:
```json
{
  "success": true,
  "wallet": {
    "balance": "2500.00",
    "last_transaction": {
      "amount": "60.00",
      "type": "DEBIT",
      "category": "MESS",
      "timestamp": "2025-11-20T12:30:00Z"
    }
  }
}
```

**Recharge Wallet**  
**Endpoint**: POST /api/v1/finance/wallet/recharge/  
**Description**: Wallet mein paisa add karna.  

**Request Body**:
```json
{
  "amount": "1000.00",
  "payment_method": "UPI",
  "transaction_id": "TXN123456789"
}
```

**Business Logic**:
```python
# apps/finance/services.py
def recharge_wallet(user, amount, payment_method, transaction_id):
    # Update wallet balance
    tenant_profile = user.tenant_profile
    tenant_profile.wallet_balance += amount
    tenant_profile.save()
    
    # Create transaction record
    WalletTransaction.objects.create(
        user=user,
        amount=amount,
        txn_type='CREDIT',
        category='RECHARGE',
        timestamp=timezone.now()
    )
    
    return tenant_profile.wallet_balance
```

#### 4.3 Credit Score System (USP 10)
**Get Credit Score**  
**Endpoint**: GET /api/v1/finance/credit-score/  
**Description**: User ka current PG credit score.  

**Business Logic**:
```python
# apps/finance/services.py
def update_credit_score(user, payment_date, due_date):
    tenant_profile = user.tenant_profile
    
    if payment_date <= due_date:
        # Reward for timely payment
        tenant_profile.pg_credit_score += 10
        if tenant_profile.pg_credit_score > 900:
            tenant_profile.pg_credit_score = 900
    else:
        # Penalty for late payment
        days_late = (payment_date - due_date).days
        penalty = min(days_late * 2, 50)  # Max 50 points penalty
        tenant_profile.pg_credit_score -= penalty
        if tenant_profile.pg_credit_score < 300:
            tenant_profile.pg_credit_score = 300
    
    tenant_profile.save()
    return tenant_profile.pg_credit_score
```

#### 4.4 Payment Processing
**Pay Invoice**  
**Endpoint**: POST /api/v1/finance/invoices/{invoice_id}/pay/  
**Description**: Invoice payment processing.  

**Request Body**:
```json
{
  "payment_method": "WALLET",
  "amount": "8560.00"
}
```

**Business Logic**:
```python
# apps/finance/services.py
def pay_invoice(invoice_id, user, payment_method, amount):
    invoice = Invoice.objects.get(id=invoice_id)
    
    if payment_method == 'WALLET':
        tenant_profile = user.tenant_profile
        if tenant_profile.wallet_balance < amount:
            raise ValidationError("Insufficient wallet balance")
        
        # Deduct from wallet
        tenant_profile.wallet_balance -= amount
        tenant_profile.save()
        
        # Create transaction
        WalletTransaction.objects.create(
            user=user,
            amount=amount,
            txn_type='DEBIT',
            category='RENT'
        )
    
    # Mark invoice as paid
    invoice.is_paid = True
    invoice.payment_date = timezone.now().date()
    invoice.save()
    
    # Update credit score
    update_credit_score(user, invoice.payment_date, invoice.month)
    
    return invoice
```

#### 4.5 Internal APIs for Other Apps
```python
# For mess app to deduct meal costs
POST /api/v1/finance/internal/wallet/deduct/
Body: {"user_id": "uuid", "amount": 60.00, "category": "MESS"}

# For booking app to process deposits
POST /api/v1/finance/internal/process-deposit/

# For operations app to process fines
POST /api/v1/finance/internal/process-fine/
```

---

## APP 5: OPERATIONS & SAFETY SERVICE (`apps/operations`)

### Models: Complaint, EntryLog, HygieneRating
Operations mein complaints, entry logging, hygiene tracking, aur safety features shamil hain.

#### 5.1 Complaint Management
**Submit Complaint**  
**Endpoint**: POST /api/v1/operations/complaints/  
**Description**: Naya complaint submit karna.  

**Request Body**:
```json
{
  "category": "PLUMBING",
  "description": "Bathroom tap is leaking continuously",
  "image": "base64_encoded_image_or_file_upload"
}
```

**Database Interaction**:
- **Complaint Table**: Naya complaint record create
- Auto-assign to manager based on category

**Response**:
```json
{
  "success": true,
  "complaint": {
    "id": "550e8400-e29b-41d4-a716-446655440040",
    "category": "PLUMBING",
    "description": "Bathroom tap is leaking continuously",
    "status": "OPEN",
    "created_at": "2025-11-20T14:30:00Z"
  }
}
```

#### 5.2 AI Chatbot Integration (USP 14)
**WhatsApp Webhook**  
**Endpoint**: POST /api/v1/operations/webhook/whatsapp/  
**Description**: WhatsApp bot se complaints receive karta hai.  

**Request Body** (from WhatsApp API):
```json
{
  "from": "+919876543210",
  "message": "My room tap is leaking",
  "timestamp": "2025-11-20T14:30:00Z"
}
```

**Business Logic**:
```python
# apps/operations/services.py
import re

def process_whatsapp_message(phone_number, message, timestamp):
    # Find user by phone number
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
    except CustomUser.DoesNotExist:
        return {"error": "User not found"}
    
    # AI/NLP to categorize complaint
    category = categorize_complaint(message)
    
    # Create complaint
    complaint = Complaint.objects.create(
        tenant=user,
        category=category,
        description=message,
        is_raised_by_bot=True,
        status='OPEN'
    )
    
    # Send confirmation message back
    response_message = f"Complaint registered with ID: {complaint.id}. Our team will resolve it soon."
    send_whatsapp_message(phone_number, response_message)
    
    return complaint

def categorize_complaint(message):
    # Simple keyword-based categorization
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['tap', 'water', 'leak', 'plumbing']):
        return 'PLUMBING'
    elif any(word in message_lower for word in ['light', 'fan', 'electric', 'power']):
        return 'ELECTRIC'
    elif any(word in message_lower for word in ['food', 'mess', 'meal']):
        return 'FOOD'
    elif any(word in message_lower for word in ['wifi', 'internet', 'network']):
        return 'WIFI'
    else:
        return 'OTHER'
```

#### 5.3 Entry Logging & Night Alerts (USP 12)
**Log Entry/Exit**  
**Endpoint**: POST /api/v1/operations/entry-log/  
**Description**: Biometric/QR scanner se entry/exit log karta hai.  

**Request Body**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "direction": "IN",
  "timestamp": "2025-11-20T23:15:00Z"
}
```

**Business Logic**:
```python
# apps/operations/services.py
from datetime import time

def log_entry_exit(user_id, direction, timestamp):
    user = CustomUser.objects.get(id=user_id)
    
    # Check if it's late entry (after 10 PM)
    entry_time = timestamp.time()
    is_late = entry_time > time(22, 0) and direction == 'IN'
    
    # Create entry log
    entry_log = EntryLog.objects.create(
        tenant=user,
        direction=direction,
        timestamp=timestamp,
        is_late_entry=is_late
    )
    
    # Send parent alert if late entry
    if is_late and user.role == 'TENANT':
        send_parent_alert(user, timestamp)
        entry_log.parent_alert_sent = True
        entry_log.save()
    
    return entry_log

def send_parent_alert(user, timestamp):
    tenant_profile = user.tenant_profile
    if tenant_profile.guardian_user:
        parent = tenant_profile.guardian_user
        
        message = f"Alert: {user.username} entered PG at {timestamp.strftime('%I:%M %p')} on {timestamp.strftime('%d/%m/%Y')}"
        
        # Send SMS to parent
        if parent.phone_number:
            send_sms(parent.phone_number, message)
```

#### 5.4 Hygiene Scorecard (USP 13)
**Submit Hygiene Rating**  
**Endpoint**: POST /api/v1/operations/hygiene/rate/  
**Description**: Daily hygiene rating submit karna (Manager only).  

**Request Body**:
```json
{
  "area_photo": "base64_encoded_image",
  "score": 4,
  "remarks": "Common area is clean, but washroom needs attention"
}
```

**Get Hygiene History**  
**Endpoint**: GET /api/v1/operations/hygiene/history/  
**Description**: Past hygiene ratings.  

**Response**:
```json
{
  "success": true,
  "hygiene_ratings": [
    {
      "date": "2025-11-20",
      "score": 4,
      "remarks": "Common area is clean, but washroom needs attention"
    }
  ],
  "average_score": 4.2
}
```

#### 5.5 Internal APIs for Other Apps
```python
# For users app to verify entry permissions
GET /api/v1/operations/internal/verify-access/{user_id}/

# For finance app to log fine-related entries
POST /api/v1/operations/internal/log-fine/
```

---

## APP 6: SMART MESS SERVICE (`apps/mess`)

### Models: MessMenu, DailyMealSelection
Smart mess mein pay-per-day meal system, menu management, aur meal analytics ke features shamil hain.

#### 6.1 Daily Menu Management
**Get Today's Menu**  
**Endpoint**: GET /api/v1/mess/menu/today/  
**Description**: Aaj ka menu with prices.  

**Response**:
```json
{
  "success": true,
  "menu": {
    "date": "2025-11-20",
    "breakfast": {
      "item": "Poha + Tea",
      "price": "40.00"
    },
    "lunch": {
      "item": "Dal Rice + Sabzi + Roti",
      "price": "70.00"
    },
    "dinner": {
      "item": "Paneer Curry + Roti + Rice",
      "price": "80.00"
    }
  }
}
```

**Create Menu (Manager Only)**  
**Endpoint**: POST /api/v1/mess/menu/create/  
**Description**: Naya daily menu create karna.  

**Request Body**:
```json
{
  "date": "2025-11-21",
  "breakfast": "Upma + Coffee",
  "lunch": "Rajma Rice + Salad",
  "dinner": "Chicken Curry + Roti",
  "price_breakfast": "45.00",
  "price_lunch": "75.00",
  "price_dinner": "90.00"
}
```

#### 6.2 Pay-Per-Day Meal Booking (USP 15 - Core Feature)
**Book Meal**  
**Endpoint**: POST /api/v1/mess/book-meal/  
**Description**: Daily meal booking with wallet deduction.  

**Request Body**:
```json
{
  "date": "2025-11-20",
  "meal_type": "LUNCH",
  "status": "EATING"
}
```

**Business Logic**:
```python
# apps/mess/services.py
from apps.finance.models import WalletTransaction

def book_meal(user, date, meal_type, status):
    # Get today's menu
    try:
        menu = MessMenu.objects.get(date=date)
    except MessMenu.DoesNotExist:
        raise ValidationError("Menu not available for this date")
    
    # Get or create daily meal selection
    selection, created = DailyMealSelection.objects.get_or_create(
        tenant=user,
        date=date,
        defaults={'total_cost': 0.00}
    )
    
    # Calculate meal cost
    meal_cost = 0
    if meal_type == 'BREAKFAST':
        meal_cost = menu.price_breakfast
        selection.breakfast_status = status
    elif meal_type == 'LUNCH':
        meal_cost = menu.price_lunch
        selection.lunch_status = status
    elif meal_type == 'DINNER':
        meal_cost = menu.price_dinner
        selection.dinner_status = status
    
    # Process payment if EATING
    if status == 'EATING':
        # Check wallet balance
        tenant_profile = user.tenant_profile
        if tenant_profile.wallet_balance < meal_cost:
            raise ValidationError("Insufficient wallet balance. Please recharge.")
        
        # Deduct from wallet
        tenant_profile.wallet_balance -= meal_cost
        tenant_profile.save()
        
        # Create transaction record
        WalletTransaction.objects.create(
            user=user,
            amount=meal_cost,
            txn_type='DEBIT',
            category='MESS'
        )
        
        # Update total cost
        selection.total_cost += meal_cost
    
    elif status == 'SKIPPING':
        # If changing from EATING to SKIPPING, refund money
        if (meal_type == 'BREAKFAST' and selection.breakfast_status == 'EATING') or \
           (meal_type == 'LUNCH' and selection.lunch_status == 'EATING') or \
           (meal_type == 'DINNER' and selection.dinner_status == 'EATING'):
            
            # Refund to wallet
            tenant_profile = user.tenant_profile
            tenant_profile.wallet_balance += meal_cost
            tenant_profile.save()
            
            # Create refund transaction
            WalletTransaction.objects.create(
                user=user,
                amount=meal_cost,
                txn_type='CREDIT',
                category='REFUND'
            )
            
            selection.total_cost -= meal_cost
    
    selection.save()
    return selection
```

**Response**:
```json
{
  "success": true,
  "message": "Lunch booked successfully!",
  "meal_selection": {
    "date": "2025-11-20",
    "lunch_status": "EATING",
    "meal_cost": "70.00",
    "remaining_wallet_balance": "2430.00"
  }
}
```

#### 6.3 Meal History & Analytics
**Get My Meal History**  
**Endpoint**: GET /api/v1/mess/my-history/  
**Description**: User ka meal history aur spending analytics.  

**Query Parameters**:
```
?start_date=2025-11-01&end_date=2025-11-30
```

**Response**:
```json
{
  "success": true,
  "analytics": {
    "total_spent": "1850.00",
    "meals_taken": 28,
    "meals_skipped": 12,
    "money_saved": "840.00",
    "average_daily_cost": "61.67"
  },
  "daily_breakdown": [
    {
      "date": "2025-11-20",
      "breakfast_status": "EATING",
      "lunch_status": "EATING", 
      "dinner_status": "SKIPPING",
      "daily_cost": "110.00"
    }
  ]
}
```

#### 6.4 Mess Management (Manager Features)
**Get Daily Meal Count**  
**Endpoint**: GET /api/v1/mess/daily-count/{date}/  
**Description**: Kitne students ne kya khana book kiya hai.  

**Response**:
```json
{
  "success": true,
  "meal_count": {
    "date": "2025-11-20",
    "breakfast": {
      "eating": 45,
      "skipping": 15
    },
    "lunch": {
      "eating": 52,
      "skipping": 8
    },
    "dinner": {
      "eating": 48,
      "skipping": 12
    }
  }
}
```

#### 6.5 Internal APIs for Other Apps
```python
# For finance app to get monthly mess totals
GET /api/v1/mess/internal/monthly-total/{user_id}/{month}/

# For operations app to check meal complaints
GET /api/v1/mess/internal/meal-feedback/{date}/
```

---

## 🔗 INTER-APP COMMUNICATION (Modular Monolith Advantage)

Microservices mein humein HTTP API calls karni padti hain, lekin modular monolith mein hum **direct Python imports** use karte hain.

### Communication Patterns

| Scenario | Source App | Target App | Method |
|----------|------------|------------|---------|
| User registration creates empty wallet | `users` | `finance` | Direct model import |
| Booking updates bed occupancy | `bookings` | `inventory` | Direct model import |
| Meal booking deducts wallet balance | `mess` | `finance` | Direct model import |
| Invoice generation gets mess total | `finance` | `mess` | Service function call |
| SOS alert gets parent contact | `users` | `users` | Model relationship |
| Entry log sends parent alert | `operations` | `users` | Service function call |

### Example: Complete Meal Booking Flow
```python
# apps/mess/services.py
from apps.finance.models import WalletTransaction
from apps.users.models import TenantProfile

def book_meal_complete_flow(user, date, meal_type, status):
    # Step 1: Get menu (mess app)
    menu = MessMenu.objects.get(date=date)
    
    # Step 2: Check wallet balance (finance app data)
    tenant_profile = user.tenant_profile  # Direct model access
    if tenant_profile.wallet_balance < menu.price_lunch:
        raise ValidationError("Insufficient balance")
    
    # Step 3: Create meal selection (mess app)
    selection = DailyMealSelection.objects.create(
        tenant=user,
        date=date,
        lunch_status=status
    )
    
    # Step 4: Deduct money (finance app)
    tenant_profile.wallet_balance -= menu.price_lunch
    tenant_profile.save()
    
    # Step 5: Create transaction log (finance app)
    WalletTransaction.objects.create(
        user=user,
        amount=menu.price_lunch,
        txn_type='DEBIT',
        category='MESS'
    )
    
    return selection
```

### Service Layer Pattern
```python
# apps/finance/services.py
def deduct_from_wallet(user, amount, category):
    """Reusable service function for wallet deduction"""
    tenant_profile = user.tenant_profile
    
    if tenant_profile.wallet_balance < amount:
        return False, "Insufficient balance"
    
    tenant_profile.wallet_balance -= amount
    tenant_profile.save()
    
    WalletTransaction.objects.create(
        user=user,
        amount=amount,
        txn_type='DEBIT',
        category=category
    )
    
    return True, tenant_profile.wallet_balance

# Usage in mess app
from apps.finance.services import deduct_from_wallet

success, balance = deduct_from_wallet(user, meal_cost, 'MESS')
if not success:
    raise ValidationError(balance)  # balance contains error message
```

---

## 📱 API RESPONSE PATTERNS

### Success Response Format
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-11-20T10:30:00Z"
  }
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Wallet balance is insufficient for this transaction",
    "details": {
      "required": "500.00",
      "available": "250.00"
    }
  }
}
```

### Pagination Response Format
```json
{
  "success": true,
  "data": [
    {"id": "uuid1", "name": "Room 101"},
    {"id": "uuid2", "name": "Room 102"}
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 50,
    "items_per_page": 10
  }
}
```

---

## 🚀 DEVELOPMENT ROADMAP (Step-by-Step Implementation)

### Phase 1: Foundation Setup (Week 1-2)
1. **Django Project Setup**
   - Create `smart_pg_backend` project
   - Setup apps structure (`users`, `inventory`, `bookings`, `finance`, `operations`, `mess`)
   - Configure PostgreSQL database
   - Setup Django REST Framework
   - Configure JWT authentication

2. **App 1: Users**
   - Create `CustomUser` and `TenantProfile` models
   - Implement registration/login APIs
   - Setup JWT token generation
   - Test parent portal access

### Phase 2: Core Business Logic (Week 3-4)
3. **App 2: Inventory**
   - Create `Room` and `Bed` models
   - Build room listing APIs
   - Implement public bed link feature (USP 3)
   - Add IoT meter reading endpoint (USP 5)

4. **App 3: Bookings**
   - Create `Booking` model
   - Build booking creation flow
   - Implement zero-deposit logic (USP 8)
   - Add digital agreement features (USP 7)

### Phase 3: Financial System (Week 5-6)
5. **App 4: Finance**
   - Create `Invoice` and `WalletTransaction` models
   - Build wallet management system
   - Implement auto-invoice generation
   - Add credit score calculation (USP 10)

6. **App 6: Smart Mess**
   - Create `MessMenu` and `DailyMealSelection` models
   - Build pay-per-day meal booking (USP 15)
   - Implement wallet integration
   - Add meal analytics

### Phase 4: Operations & Safety (Week 7-8)
7. **App 5: Operations**
   - Create `Complaint`, `EntryLog`, `HygieneRating` models
   - Build complaint management system
   - Implement entry logging with alerts (USP 12)
   - Add WhatsApp bot integration (USP 14)

8. **Integration & Testing**
   - Test inter-app communication
   - Implement error handling
   - Add comprehensive logging
   - Performance optimization
   - API documentation

---

## 📋 MODELS DISTRIBUTION SUMMARY

**Total**: 12 models across 6 Django apps

| App | Models Count | Models |
|-----|--------------|--------|
| User Management | 2 | CustomUser, TenantProfile |
| Property & Inventory | 2 | Room, Bed |
| Booking Management | 1 | Booking |
| Finance Management | 2 | Invoice, WalletTransaction |
| Operations & Safety | 3 | Complaint, EntryLog, HygieneRating |
| Smart Mess | 2 | MessMenu, DailyMealSelection |

---

## 🎯 KEY TAKEAWAYS FOR DEVELOPERS

### Modular Monolith Benefits
1. **Single Database**: No distributed transaction complexity
2. **Direct Imports**: Fast inter-app communication
3. **Shared Models**: Easy data relationships across apps
4. **Simple Deployment**: One application to deploy
5. **Easy Debugging**: All code in one place

### Best Practices
1. **Use Service Layer**: Business logic in `services.py` files
2. **Model Relationships**: Leverage Django's ForeignKey, OneToOne
3. **Transaction Management**: Use `@transaction.atomic` for data consistency
4. **Error Handling**: Consistent error responses across all apps
5. **API Versioning**: Use `/api/v1/` prefix for future compatibility

### Development Guidelines
- Each app should have clear boundaries
- Use Django signals for cross-app notifications
- Implement proper logging for debugging
- Write comprehensive tests for each app
- Document all API endpoints

**✅ SERVICE DOCUMENTATION COMPLETE**

Ye documentation ek complete guide hai Smart PG Management System ke liye. Har app ka purpose, models, APIs, aur inter-app communication clearly explain kiya gaya hai. Isse follow karke ek beginner bhi easily system develop kar sakta hai! 🚀