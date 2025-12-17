# 🏨 Smart PG Management System - Service Documentation (Modular Monolith)

## 1. INTRODUCTION

Ye documentation **Smart PG Management System** ke liye hai, jisme **18 independent Django apps** ka detailed description diya gaya hai. Ye apps modular monolith architecture follow karti hain with **40+ Django models** across different apps.

### 1.1 Project Overview
- **Architecture Type**: Modular Monolith Architecture (Django)
- **Total Apps**: 18 Feature Apps + 1 Core Settings
- **Total Models**: 40+ database models
- **Communication**: Direct Python Imports (Synchronous)
- **Database**: MySQL (single database)
- **Authentication**: JWT-based
- **Language**: Python 3.10+ with Django 4.2+
- **Multi-Language Support**: English, Hindi, Tamil, Telugu, Kannada, Bengali

### 1.2 Technology Stack
- **Backend Framework**: Django REST Framework
- **ORM**: Django ORM
- **Database**: MySQL (production) / SQLite (development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Validation**: Django REST Framework serializers
- **File Storage**: Django FileField/ImageField + AWS S3 (for documents)
- **Task Queue**: Celery (for background tasks like report generation)
- **Caching**: Redis (optional)
- **Internationalization**: Django i18n framework

---

## APP 1: USER MANAGEMENT SERVICE (`apps/users`)

**Purpose**: User authentication, role management, profiles, and parent portal access.

**Database Tables**: CustomUser, TenantProfile, StaffProfile

### 1.1 User Registration
**Endpoint**: POST /api/v1/auth/register/  
**Description**: Register new users (Admin, Manager, Tenant, Parent)

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

**Database Tables Involved**:
- CustomUser: Create new user record with hashed password
- TenantProfile: Auto-create if role = 'TENANT'

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

### 1.2 User Login
**Endpoint**: POST /api/v1/auth/login/  
**Description**: Authenticate users and generate JWT tokens

**Request Body**:
```json
{
  "username": "rahul_sharma",
  "password": "Pass@123"
}
```

**Database Tables Involved**:
- CustomUser: Fetch user by username, verify password

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

### 1.3 Aadhaar Upload & Police Verification (USP 2)
**Endpoint**: POST /api/v1/auth/aadhaar/upload/  
**Description**: Upload Aadhaar card and trigger police verification

**Request Body**:
```json
{
  "aadhaar_number": "1234-5678-9012",
  "aadhaar_front_image": "base64_encoded_image",
  "aadhaar_back_image": "base64_encoded_image"
}
```

**Database Tables Involved**:
- TenantProfile: Update aadhaar_number, aadhaar_document_url
- Update police_verification_status to 'SUBMITTED'

### 1.4 Parent Portal Access (USP 1)
**Endpoint**: GET /api/v1/auth/parent/my-wards/  
**Description**: Parents can view their children's details

**Database Tables Involved**:
- TenantProfile: Filter by guardian_user = current_user

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

### 1.5 SOS Alert System (USP 11)
**Endpoint**: POST /api/v1/auth/sos/trigger/  
**Description**: Emergency alert system for student safety

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

**Database Tables Involved**:
- TenantProfile: Get guardian contact
- CustomUser: Get manager contact
- NotificationLog: Store alert record

---

## APP 2: PROPERTY SERVICE (`apps/properties`)

**Purpose**: Property management including branches, rooms, beds, assets, and IoT integration for multi-property PG chains.

**Database Tables**: Property, Room, Bed, PricingRule, Asset, ElectricityReading

### 2.1 Create Property (First Step)
**Endpoint**: POST /api/v1/properties/create/  
**Description**: Create new PG property/branch

**Request Body**:
```json
{
  "name": "Gokuldham PG 1",
  "address": "123 Main Street, Delhi",
  "total_floors": 4,
  "contact_number": "+919876543210",
  "owner_id": "uuid-owner-id"
}
```

**Database Tables Involved**:
- Property: Create new property record

### 2.2 Add Rooms to Property
**Endpoint**: POST /api/v1/properties/{property_id}/rooms/create/  
**Description**: Add rooms to a specific property

**Request Body**:
```json
{
  "room_number": "204-B",
  "floor": 2,
  "capacity": 2,
  "has_ac": true,
  "has_balcony": false,
  "base_rent": "8000.00"
}
```

**Database Tables Involved**:
- Room: Create room linked to property
- Auto-generate beds based on capacity

### 2.3 Add Beds to Room
**Endpoint**: POST /api/v1/properties/rooms/{room_id}/beds/create/  
**Description**: Add individual beds to room

**Request Body**:
```json
{
  "bed_label": "A",
  "iot_meter_id": "IOT-METER-X99"
}
```

**Database Tables Involved**:
- Bed: Create bed record linked to room

### 2.4 List Available Rooms
**Endpoint**: GET /api/v1/properties/rooms/  
**Description**: Get available rooms with filters

**Query Parameters**:
```
?floor=2&has_ac=true&capacity=2&available=true&property_id=uuid
```

**Database Tables Involved**:
- Property: Validation
- Room: Filter rooms by criteria
- Bed: Check availability count

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

### 2.5 Live Vacant Bed Link (USP 3)
**Endpoint**: GET /api/v1/properties/public/bed/{public_uid}/  
**Description**: Public link for bed details without login

**Database Tables Involved**:
- Bed: Get bed by public_uid
- Room, Property: Related data

### 2.6 Dynamic Pricing Engine (USP 4)
**Endpoint**: PUT /api/v1/properties/rooms/{room_id}/pricing/  
**Description**: Update seasonal pricing

**Request Body**:
```json
{
  "pricing_rule": "SUMMER_SURGE",
  "multiplier": 1.2,
  "effective_from": "2025-06-01",
  "effective_to": "2025-08-31"
}
```

**Database Tables Involved**:
- PricingRule: Create/update pricing rule
- Room: Update current_seasonal_rent

### 2.7 Smart Electricity Meter (USP 5)
**Endpoint**: POST /api/v1/properties/iot/meter-reading/  
**Description**: Receive IoT electricity readings

**Request Body**:
```json
{
  "meter_id": "IOT-METER-X99",
  "current_reading": 1250.75,
  "timestamp": "2025-11-20T10:30:00Z"
}
```

**Database Tables Involved**:
- Bed: Find bed by iot_meter_id
- ElectricityReading: Store new reading

### 2.8 Asset Management (Advanced Feature 4)
**Endpoint**: POST /api/v1/properties/assets/create/  
**Description**: Add new asset to property

**Request Body**:
```json
{
  "name": "Voltas AC",
  "category": "APPLIANCE",
  "room_id": "uuid-room-id",
  "purchase_date": "2025-01-15",
  "warranty_expiry": "2027-01-15",
  "qr_code": "ASSET-AC-001"
}
```

**Database Tables Involved**:
- Asset: Create asset record

### 2.9 Asset QR Code Scan
**Endpoint**: GET /api/v1/properties/assets/scan/{qr_code}/  
**Description**: Scan QR code to get asset details and service history

**Database Tables Involved**:
- Asset: Get asset by QR code
- AssetServiceHistory: Get service records

**Response**:
```json
{
  "success": true,
  "asset": {
    "name": "Voltas AC",
    "room_number": "204-B",
    "next_service_due": "2025-12-01",
    "warranty_status": "ACTIVE"
  },
  "service_history": [
    {
      "date": "2025-06-01",
      "type": "MAINTENANCE",
      "description": "Gas refill and cleaning"
    }
  ]
}
```

### 2.10 Multi-Property Dashboard (Advanced Feature 1)
**Endpoint**: GET /api/v1/properties/dashboard/unified/  
**Description**: Combined data for all properties

**Database Tables Involved**:
- Property: Get all properties for owner
- Room, Bed: Calculate occupancy metrics
- Invoice: Calculate revenue

**Response**:
```json
{
  "success": true,
  "unified_view": {
    "total_properties": 3,
    "total_revenue": "1275000.00",
    "total_rooms": 150,
    "total_occupied": 128,
    "total_available": 22,
    "overall_occupancy_rate": 85.33
  }
}
```

### 2.11 Branch Switcher
**Endpoint**: GET /api/v1/properties/dashboard/switch/{property_id}/  
**Description**: Switch to specific property dashboard

**Database Tables Involved**:
- Property: Get specific property data
- Room, Bed: Calculate metrics for property

---

## APP 3: BOOKING MANAGEMENT SERVICE (`apps/bookings`)

**Purpose**: Complete booking lifecycle from room allocation to tenant exit with AI compatibility matching and digital agreements.

**Database Tables**: Booking, DigitalAgreement

### 3.1 AI Compatibility Matching (USP 6)
**Endpoint**: POST /api/v1/bookings/compatibility-match/  
**Description**: Find compatible roommates using AI

**Request Body**:
```json
{
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "preferences": {
    "sleep_schedule": "NIGHT_OWL",
    "cleanliness_level": "HIGH",
    "noise_tolerance": "LOW",
    "study_hours": "LATE_NIGHT"
  }
}
```

**Database Tables Involved**:
- Bed: Get occupied beds with available space
- TenantProfile: Get current tenant preferences
- Calculate compatibility scores

**Response**:
```json
{
  "success": true,
  "recommended_rooms": [
    {
      "room_number": "204-B",
      "compatibility_score": 100,
      "current_roommate": "Rohan Das",
      "matching_traits": ["Night Owl", "High Cleanliness", "Late Night Studier"]
    }
  ]
}
```

### 3.2 Create Booking
**Endpoint**: POST /api/v1/bookings/create/  
**Description**: Create new booking with multiple payment options

**Request Body**:
```json
{
  "bed_id": "550e8400-e29b-41d4-a716-446655440020",
  "start_date": "2025-12-01",
  "payment_mode": "FINTECH_LOAN",
  "loan_provider_name": "PayLater Finance"
}
```

**Database Tables Involved**:
- Bed: Check availability and mark as occupied
- Booking: Create booking record
- Transaction: Handle payment based on mode

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

### 3.3 Digital Agreement Generation (USP 7)
**Endpoint**: POST /api/v1/bookings/{booking_id}/agreement/  
**Description**: Generate digital agreement with eSign

**Database Tables Involved**:
- DigitalAgreement: Store agreement file and signature status
- Booking: Link agreement to booking

### 3.4 Zero-Deposit Option (USP 8)
**Endpoint**: POST /api/v1/bookings/{booking_id}/fintech-approval/  
**Description**: Process fintech loan approval for zero deposit

**Request Body**:
```json
{
  "loan_provider": "PayLater Finance",
  "loan_amount": "15000.00",
  "approval_status": "APPROVED"
}
```

**Database Tables Involved**:
- Booking: Update status to ACTIVE
- Transaction: Record loan transaction

### 3.5 Digital Notice Period & Auto Refund (USP 9)
**Endpoint**: POST /api/v1/bookings/{booking_id}/request-exit/  
**Description**: Request exit with automatic refund calculation

**Request Body**:
```json
{
  "exit_date": "2025-12-15",
  "reason": "Course completed"
}
```

**Database Tables Involved**:
- Booking: Update notice_given_date, calculate refund
- Transaction: Process refund transaction
- Bed: Mark as available

---

## APP 4: FINANCE SERVICE (`apps/finance`)

**Purpose**: Complete financial management including invoices, wallet system, expense tracking, and credit scoring.

**Database Tables**: Invoice, Transaction, Expense, WalletTransaction

### 4.1 Auto Invoice Generation (Monthly Cron)
**Endpoint**: POST /api/v1/finance/generate-monthly-invoices/  
**Description**: Generate invoices for all active bookings (1st of every month)

**Database Tables Involved**:
- Booking: Get all active bookings
- ElectricityReading: Calculate electricity usage
- DailyMealSelection: Get mess charges
- Invoice: Create monthly invoice

### 4.2 Wallet Management
**Endpoint**: GET /api/v1/finance/wallet/balance/  
**Description**: Get current wallet balance

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

### 4.3 Wallet Recharge
**Endpoint**: POST /api/v1/finance/wallet/recharge/  
**Description**: Add money to wallet

**Request Body**:
```json
{
  "amount": "1000.00",
  "payment_method": "UPI",
  "transaction_id": "TXN123456789"
}
```

**Database Tables Involved**:
- Transaction: Create credit transaction
- TenantProfile: Update wallet_balance

### 4.4 Credit Score System (USP 10)
**Endpoint**: GET /api/v1/finance/credit-score/  
**Description**: Get tenant's PG credit score

**Database Tables Involved**:
- TenantProfile: Get current pg_credit_score
- Invoice: Check payment history for score calculation

**Response**:
```json
{
  "success": true,
  "credit_score": {
    "current_score": 750,
    "score_category": "EXCELLENT",
    "factors": {
      "timely_payments": 85,
      "complaint_history": 10,
      "tenure": 5
    }
  }
}
```

### 4.5 Pay Invoice
**Endpoint**: POST /api/v1/finance/invoices/{invoice_id}/pay/  
**Description**: Process invoice payment

**Request Body**:
```json
{
  "payment_method": "WALLET",
  "amount": "8560.00"
}
```

**Database Tables Involved**:
- Invoice: Mark as paid, update payment_date
- Transaction: Create payment transaction
- TenantProfile: Update wallet_balance and credit_score

### 4.6 Expense Tracking (Advanced Feature 2)
**Endpoint**: POST /api/v1/finance/expenses/add/  
**Description**: Log property expenses

**Request Body**:
```json
{
  "category": "MAINTENANCE",
  "amount": "5000.00",
  "description": "AC repair in Room 204",
  "receipt_image": "base64_encoded_image"
}
```

**Database Tables Involved**:
- Expense: Create expense record

---

## APP 5: OPERATIONS SERVICE (`apps/operations`)

**Purpose**: Daily operations including complaints, safety features, entry logging, and AI chatbot integration.

**Database Tables**: Complaint, EntryLog, Notice, ChatLog

### 5.1 Submit Complaint
**Endpoint**: POST /api/v1/operations/complaints/  
**Description**: Submit new complaint

**Request Body**:
```json
{
  "category": "PLUMBING",
  "description": "Bathroom tap is leaking continuously",
  "image": "base64_encoded_image_or_file_upload"
}
```

**Database Tables Involved**:
- Complaint: Create complaint record
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

### 5.2 Entry/Exit Logging & Night Alerts (USP 12)
**Endpoint**: POST /api/v1/operations/entry-log/  
**Description**: Log biometric/QR entry with parent alerts

**Request Body**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "direction": "IN",
  "timestamp": "2025-11-20T23:15:00Z"
}
```

**Database Tables Involved**:
- EntryLog: Create entry record
- TenantProfile: Get guardian contact for late entry alerts
- NotificationLog: Send parent alert if after 10 PM

### 5.3 Hygiene Scorecard (USP 13)
**Endpoint**: POST /api/v1/operations/hygiene/rate/  
**Description**: Submit daily hygiene rating (Manager only)

**Request Body**:
```json
{
  "area_photo": "base64_encoded_image",
  "score": 4,
  "remarks": "Common area is clean, but washroom needs attention"
}
```

**Database Tables Involved**:
- HygieneInspection: Store daily hygiene rating

### 5.4 AI Chatbot Integration (USP 14)
**Endpoint**: POST /api/v1/operations/webhook/whatsapp/  
**Description**: WhatsApp bot webhook for complaints

**Request Body**:
```json
{
  "from": "+919876543210",
  "message": "My room tap is leaking",
  "timestamp": "2025-11-20T14:30:00Z"
}
```

**Database Tables Involved**:
- CustomUser: Find user by phone number
- Complaint: Auto-create complaint from message
- ChatLog: Store bot interaction

### 5.5 Digital Notice Board (Advanced Feature 7)
**Endpoint**: GET /api/v1/operations/notices/  
**Description**: Get active notices

**Database Tables Involved**:
- Notice: Filter by property and published status

---

## APP 6: SMART MESS SERVICE (`apps/mess`)

**Purpose**: Revolutionary pay-per-day mess system with wallet integration and meal analytics.

**Database Tables**: MessMenu, DailyMealSelection

### 6.1 Create Daily Menu (Manager)
**Endpoint**: POST /api/v1/mess/menu/create/  
**Description**: Create daily menu with prices

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

**Database Tables Involved**:
- MessMenu: Create daily menu record

### 6.2 Get Today's Menu
**Endpoint**: GET /api/v1/mess/menu/today/  
**Description**: Get current day's menu with prices

**Database Tables Involved**:
- MessMenu: Get menu for current date

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

### 6.3 Pay-Per-Day Meal Booking (USP 15 - Core Feature)
**Endpoint**: POST /api/v1/mess/book-meal/  
**Description**: Book daily meals with wallet deduction

**Request Body**:
```json
{
  "date": "2025-11-20",
  "meal_type": "LUNCH",
  "status": "EATING"
}
```

**Database Tables Involved**:
- MessMenu: Get meal price for the date
- DailyMealSelection: Create/update meal selection
- TenantProfile: Deduct from wallet_balance
- WalletTransaction: Record transaction

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

### 6.4 Meal History & Analytics
**Endpoint**: GET /api/v1/mess/my-history/  
**Description**: Get meal history and spending analytics

**Query Parameters**:
```
?start_date=2025-11-01&end_date=2025-11-30
```

**Database Tables Involved**:
- DailyMealSelection: Get user's meal history
- Calculate analytics (total spent, meals taken/skipped)

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
  }
}
```

### 6.5 Daily Meal Count (Manager)
**Endpoint**: GET /api/v1/mess/daily-count/{date}/  
**Description**: Get meal booking count for kitchen planning

**Database Tables Involved**:
- DailyMealSelection: Count eating vs skipping for each meal

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

---

## APP 7: CRM & LEAD MANAGEMENT (`apps/crm`)

**Purpose**: Lead capture and follow-up system for enquiry management across multiple properties.

**Database Tables**: Lead

### 7.1 Create Lead
**Endpoint**: POST /api/v1/crm/leads/  
**Description**: Capture new enquiry from website or manager

**Request Body**:
```json
{
  "property_id": "uuid-of-property",
  "full_name": "Rohan Das",
  "phone_number": "9876543210",
  "email": "rohan@gmail.com",
  "status": "NEW",
  "notes": "Looking for AC room"
}
```

**Database Tables Involved**:
- Lead: Create lead record
- Check for duplicate leads by phone and property

### 7.2 List All Leads
**Endpoint**: GET /api/v1/crm/leads/  
**Description**: Get all leads with filtering options

**Query Parameters**:
```
?status=NEW&property_id=uuid&created_after=2025-11-01
```

**Database Tables Involved**:
- Lead: Filter leads by status, property, date range

### 7.3 Update Lead Status
**Endpoint**: PATCH /api/v1/crm/leads/{lead_id}/  
**Description**: Update lead status after follow-up

**Request Body**:
```json
{
  "status": "VISITED",
  "notes": "Visited today, liked Room 101. Will decide tomorrow."
}
```

**Database Tables Involved**:
- Lead: Update status and notes

### 7.4 Lead Follow-up Reminders
**Endpoint**: GET /api/v1/crm/leads/follow-up-due/  
**Description**: Get leads that need follow-up

**Database Tables Involved**:
- Lead: Get leads with follow_up_date <= today

---

## APP 8: NOTIFICATIONS (`apps/notifications`)

**Purpose**: Centralized notification system for SMS, WhatsApp, and push notifications.

**Database Tables**: NotificationLog, FCMToken

### 8.1 Register FCM Token
**Endpoint**: POST /api/v1/notifications/device/register/  
**Description**: Register device for push notifications

**Request Body**:
```json
{
  "token": "fcm-token-xyz-123",
  "device_type": "ANDROID"
}
```

**Database Tables Involved**:
- FCMToken: Store device token for user

### 8.2 Send Push Notification
**Endpoint**: POST /api/v1/notifications/push/send/  
**Description**: Send push notification to specific users

**Request Body**:
```json
{
  "user_ids": ["uuid1", "uuid2"],
  "title": "Rent Due Reminder",
  "message": "Your rent is due tomorrow",
  "type": "RENT_REMINDER"
}
```

**Database Tables Involved**:
- FCMToken: Get device tokens for users
- NotificationLog: Store notification record

### 8.3 Send SMS/WhatsApp
**Endpoint**: POST /api/v1/notifications/sms/send/  
**Description**: Send SMS or WhatsApp message

**Request Body**:
```json
{
  "phone_numbers": ["+919876543210"],
  "message": "Your rent payment is overdue",
  "type": "SMS"
}
```

**Database Tables Involved**:
- NotificationLog: Store SMS record

### 8.4 Get Notification History
**Endpoint**: GET /api/v1/notifications/history/  
**Description**: Get user's notification history

**Database Tables Involved**:
- NotificationLog: Get user's notifications

---

## APP 9: VISITOR MANAGEMENT (`apps/visitors`)

**Purpose**: Security gate management with visitor approval system.

**Database Tables**: VisitorRequest

### 9.1 Create Visitor Request
**Endpoint**: POST /api/v1/visitors/request/  
**Description**: Guard creates visitor request

**Request Body**:
```json
{
  "visitor_name": "John Doe",
  "visitor_phone": "9876543210",
  "tenant_id": "uuid-tenant-id",
  "purpose": "Friend visit"
}
```

**Database Tables Involved**:
- VisitorRequest: Create visitor request
- Send notification to tenant for approval

### 9.2 Approve/Reject Visitor
**Endpoint**: POST /api/v1/visitors/{request_id}/approve/  
**Description**: Tenant approves or rejects visitor

**Request Body**:
```json
{
  "action": "APPROVE",
  "remarks": "Friend coming for study"
}
```

**Database Tables Involved**:
- VisitorRequest: Update status and remarks

---

## APP 10: INVENTORY MANAGEMENT (`apps/inventory`)

**Purpose**: Kitchen and housekeeping stock management for consumable items.

**Database Tables**: InventoryItem, InventoryTransaction

### 10.1 Add Inventory Item
**Endpoint**: POST /api/v1/inventory/items/  
**Description**: Add new inventory item

**Request Body**:
```json
{
  "name": "Basmati Rice",
  "category": "GROCERIES",
  "unit": "KG",
  "current_stock": 50,
  "minimum_threshold": 10
}
```

**Database Tables Involved**:
- InventoryItem: Create inventory item

### 10.2 List Inventory Items
**Endpoint**: GET /api/v1/inventory/items/  
**Description**: Get all inventory items with stock levels

**Query Parameters**:
```
?category=GROCERIES&low_stock=true
```

**Database Tables Involved**:
- InventoryItem: Get items, filter by category or low stock

### 10.3 Update Stock
**Endpoint**: POST /api/v1/inventory/transactions/  
**Description**: Record stock in/out transaction

**Request Body**:
```json
{
  "item_id": "uuid-item-id",
  "transaction_type": "OUT",
  "quantity": 5,
  "remarks": "Used for daily cooking"
}
```

**Database Tables Involved**:
- InventoryTransaction: Record transaction
- InventoryItem: Update current_stock

### 10.4 Low Stock Alerts
**Endpoint**: GET /api/v1/inventory/low-stock-alerts/  
**Description**: Get items with stock below minimum threshold

**Database Tables Involved**:
- InventoryItem: Filter items where current_stock <= minimum_threshold

---

## APP 11: PAYROLL MANAGEMENT (`apps/payroll`)

**Purpose**: Staff attendance and salary management system.

**Database Tables**: StaffAttendance, SalaryPayment

### 11.1 Mark Attendance
**Endpoint**: POST /api/v1/payroll/attendance/  
**Description**: Staff marks attendance with selfie

**Request Body**:
```json
{
  "staff_id": "uuid-staff-id",
  "check_in_time": "2025-11-20T09:00:00Z",
  "selfie_image": "base64_encoded_image"
}
```

**Database Tables Involved**:
- StaffAttendance: Record attendance

### 11.2 Generate Salary
**Endpoint**: POST /api/v1/payroll/salary/generate/  
**Description**: Generate monthly salary based on attendance

**Database Tables Involved**:
- StaffAttendance: Calculate working days
- SalaryPayment: Generate salary record

---

## APP 12: HYGIENE MANAGEMENT (`apps/hygiene`)

**Purpose**: Quality control through hygiene inspections and scoring.

**Database Tables**: HygieneInspection

### 12.1 Submit Inspection
**Endpoint**: POST /api/v1/hygiene/inspections/  
**Description**: Submit hygiene inspection report

**Request Body**:
```json
{
  "area": "COMMON_AREA",
  "score": 4,
  "photo": "base64_encoded_image",
  "remarks": "Clean but needs minor touch-up"
}
```

**Database Tables Involved**:
- HygieneInspection: Store inspection record

---

## APP 13: FEEDBACK MANAGEMENT (`apps/feedback`)

**Purpose**: Collect and manage tenant feedback for continuous improvement.

**Database Tables**: ComplaintFeedback, MessFeedback

### 13.1 Submit Complaint Feedback
**Endpoint**: POST /api/v1/feedback/complaint/{complaint_id}/  
**Description**: Submit feedback after complaint resolution

**Request Body**:
```json
{
  "rating": 5,
  "comments": "Manager resolved the issue quickly",
  "resolution_satisfaction": "EXCELLENT"
}
```

**Database Tables Involved**:
- ComplaintFeedback: Store complaint feedback
- Complaint: Update feedback_given status

### 13.2 Submit Mess Feedback
**Endpoint**: POST /api/v1/feedback/mess/  
**Description**: Submit daily mess feedback

**Request Body**:
```json
{
  "date": "2025-11-20",
  "meal_type": "LUNCH",
  "rating": 4,
  "comments": "Dal was good but could be warmer"
}
```

**Database Tables Involved**:
- MessFeedback: Store mess feedback

### 13.3 Get Feedback Analytics
**Endpoint**: GET /api/v1/feedback/analytics/  
**Description**: Get feedback analytics for management

**Query Parameters**:
```
?type=MESS&start_date=2025-11-01&end_date=2025-11-30
```

**Database Tables Involved**:
- MessFeedback, ComplaintFeedback: Aggregate ratings and comments

---

## APP 14: AUDIT LOGS (`apps/audit`)

**Purpose**: Track all system activities for security and compliance.

**Database Tables**: AuditLog

### 14.1 Activity Logging (Automatic)
**Description**: Automatically logs all user activities

**Database Tables Involved**:
- AuditLog: Store user actions, timestamps, and changes

---

## APP 15: ALUMNI NETWORK (`apps/alumni`)

**Purpose**: Connect ex-tenants for job referrals and networking.

**Database Tables**: AlumniProfile, JobReferral

### 15.1 Create Alumni Profile
**Endpoint**: POST /api/v1/alumni/profile/  
**Description**: Create alumni profile after checkout

**Request Body**:
```json
{
  "current_company": "Google",
  "designation": "Software Engineer",
  "linkedin_profile": "https://linkedin.com/in/johndoe",
  "graduation_year": 2025,
  "course": "Computer Science"
}
```

**Database Tables Involved**:
- AlumniProfile: Create alumni record

### 15.2 Alumni Job Referrals
**Endpoint**: POST /api/v1/alumni/job-referrals/  
**Description**: Alumni can post job referral opportunities

**Request Body**:
```json
{
  "company_name": "Google",
  "position": "Software Engineer Intern",
  "description": "Looking for Python developers",
  "application_deadline": "2025-12-31",
  "contact_email": "referral@example.com"
}
```

**Database Tables Involved**:
- JobReferral: Create job referral record

### 15.3 Get Alumni Network
**Endpoint**: GET /api/v1/alumni/network/  
**Description**: Get alumni network for current tenants

**Query Parameters**:
```
?company=Google&graduation_year=2024
```

**Database Tables Involved**:
- AlumniProfile: Get alumni profiles with filters

### 15.4 Get Job Referrals
**Endpoint**: GET /api/v1/alumni/job-referrals/  
**Description**: Get available job referrals

**Database Tables Involved**:
- JobReferral: Get active job referrals

---

## APP 16: SAAS MANAGEMENT (`apps/saas`)

**Purpose**: Subscription and multi-tenant management for software licensing.

**Database Tables**: SubscriptionPlan, PropertySubscription

### 16.1 Create Subscription Plan
**Endpoint**: POST /api/v1/saas/plans/  
**Description**: Create new subscription plan (Super Admin only)

**Request Body**:
```json
{
  "name": "Gold Plan",
  "price": "5000.00",
  "duration_months": 12,
  "features": ["CRM", "Reports", "Multi-Property"],
  "max_properties": 5
}
```

**Database Tables Involved**:
- SubscriptionPlan: Create plan record

### 16.2 Subscribe Property
**Endpoint**: POST /api/v1/saas/subscribe/  
**Description**: Subscribe property to a plan

**Request Body**:
```json
{
  "property_id": "uuid-property-id",
  "plan_id": "uuid-plan-id",
  "payment_method": "CARD"
}
```

**Database Tables Involved**:
- PropertySubscription: Create subscription record
- Property: Update subscription status

### 16.3 Check Feature Access
**Endpoint**: GET /api/v1/saas/features/{property_id}/  
**Description**: Check which features are available for property

**Database Tables Involved**:
- PropertySubscription: Get active subscription
- SubscriptionPlan: Get plan features

### 16.4 Manage Subscriptions
**Endpoint**: GET /api/v1/saas/subscriptions/  
**Description**: Get all property subscriptions (Super Admin)

**Database Tables Involved**:
- PropertySubscription: Get all subscriptions
- Property: Get property details

---

## APP 17: REPORTS & ANALYTICS (`apps/reports`)

**Purpose**: Generate business reports and analytics for decision making.

**Database Tables**: GeneratedReport

### 17.1 Generate Revenue Report
**Endpoint**: POST /api/v1/reports/revenue/  
**Description**: Generate monthly revenue report

**Request Body**:
```json
{
  "property_id": "uuid-property-id",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "format": "PDF"
}
```

**Database Tables Involved**:
- Invoice: Get payment data
- Booking: Get tenant data
- GeneratedReport: Store report metadata

### 17.2 Generate Expense Report
**Endpoint**: POST /api/v1/reports/expenses/  
**Description**: Generate expense report for CA/accounting

**Request Body**:
```json
{
  "property_id": "uuid-property-id",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "format": "EXCEL"
}
```

**Database Tables Involved**:
- Expense: Get expense data
- GeneratedReport: Store report metadata

### 17.3 Generate Occupancy Trends
**Endpoint**: GET /api/v1/reports/occupancy-trends/  
**Description**: Get occupancy trends over time

**Query Parameters**:
```
?property_id=uuid&months=6
```

**Database Tables Involved**:
- Booking: Get historical booking data
- Room, Bed: Calculate occupancy rates

**Response**:
```json
{
  "success": true,
  "trends": [
    {
      "month": "2025-06",
      "occupancy_rate": 85.5,
      "total_revenue": "425000.00"
    },
    {
      "month": "2025-07",
      "occupancy_rate": 92.3,
      "total_revenue": "465000.00"
    }
  ]
}
```

### 17.4 Export Data
**Endpoint**: GET /api/v1/reports/export/{report_id}/  
**Description**: Download generated report

**Database Tables Involved**:
- GeneratedReport: Get report file path

---

## APP 18: LOCALIZATION (`apps/localization`)

**Purpose**: Multi-language support for 6 Indian languages.

**Database Tables**: TranslationString

### 18.1 Get Translations
**Endpoint**: GET /api/v1/localization/translations/  
**Description**: Get UI translations for user's language

**Query Parameters**:
```
?language=hi&module=mess
```

**Database Tables Involved**:
- TranslationString: Get translations by language and module

**Response**:
```json
{
  "success": true,
  "translations": {
    "book_meal": "भोजन बुक करें",
    "wallet_balance": "वॉलेट बैलेंस",
    "pay_rent": "किराया भुगतान"
  }
}
```

### 18.2 Update Translation
**Endpoint**: PUT /api/v1/localization/translations/  
**Description**: Update translation strings (Admin only)

**Request Body**:
```json
{
  "module": "mess",
  "key": "book_meal",
  "language": "hi",
  "value": "भोजन बुक करें"
}
```

**Database Tables Involved**:
- TranslationString: Update translation value

---

## COMPLETE FEATURE MAPPING

### ✅ All 15 USP Features Covered:
1. **Parent Portal Access** (App 1: Users)
2. **Aadhaar + Police Verification** (App 1: Users)
3. **Live Vacant Bed Link** (App 2: Properties)
4. **Dynamic Pricing Engine** (App 2: Properties)
5. **Smart Electricity Billing** (App 2: Properties)
6. **AI Compatibility Matching** (App 3: Bookings)
7. **Digital Agreement (eSign)** (App 3: Bookings)
8. **Zero-Deposit Option** (App 3: Bookings)
9. **Digital Notice Period & Auto Refund** (App 3: Bookings)
10. **Tenant Credit Score** (App 4: Finance)
11. **SOS Alert System** (App 1: Users)
12. **Biometric Entry + Night Alerts** (App 5: Operations)
13. **Hygiene Scorecard** (App 5: Operations)
14. **AI Chatbot (WhatsApp)** (App 5: Operations)
15. **Pay-per-Day Mess Wallet** (App 6: Mess)

### ✅ All 9 Advanced Features Covered:
1. **Multi-Property Management** (App 2: Properties)
2. **Expense Management** (App 4: Finance)
3. **Staff & Payroll Management** (App 11: Payroll)
4. **Asset & Inventory Management** (Apps 2 & 10)
5. **CRM & Lead Management** (App 7: CRM)
6. **Visitor Management** (App 9: Visitors)
7. **Digital Notice Board** (App 5: Operations)
8. **Reporting & Analytics** (App 17: Reports)
9. **Alumni Network** (App 15: Alumni)

### ✅ All 9 Technical Features Covered:
1. **Notification System** (App 8: Notifications)
2. **Offline First Architecture** (Built into all apps)
3. **Legal & KYC Compliance** (App 1: Users)
4. **Payment Settlements & Refunds** (App 4: Finance)
5. **Version Control & App Updates** (App 16: SaaS)
6. **Localization** (App 18: Localization)
7. **Audit Logs** (App 14: Audit)
8. **SaaS Subscription Model** (App 16: SaaS)
9. **Feedback & Rating Loop** (App 13: Feedback)

## DEVELOPMENT SEQUENCE SUMMARY

### Phase 1: Foundation (2-3 months)
1. **Users App**: Authentication and role management
2. **Properties App**: Property and room management
3. **Basic Finance**: Wallet and transactions

### Phase 2: Core Features (3-4 months)
4. **Bookings App**: Complete booking lifecycle
5. **Operations App**: Complaints and safety features
6. **Mess App**: Pay-per-day meal system

### Phase 3: Advanced Features (2-3 months)
7. **CRM, Visitors, Inventory**: Business scaling features
8. **Payroll, Hygiene, Feedback**: Quality management
9. **Notifications**: Communication system

### Phase 4: Enterprise Features (1-2 months)
10. **Audit, Alumni, SaaS**: Enterprise features
11. **Reports, Localization**: Analytics and multi-language
12. **Testing and Deployment**: Final polish

---

**📝 Document Version:** 3.0 (Development Sequence Optimized)  
**📅 Last Updated:** December 2025  
**🎯 Total Endpoints:** 50+ API endpoints  
**✅ Development Ready:** 100% sequenced for coding