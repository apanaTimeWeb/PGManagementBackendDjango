# 🏨 Smart PG Management System - Complete Django Folder Structure

**Architecture**: Django REST Framework with Class-Based Views (Modular Monolith)  
**Apps**: 18 Independent Feature Apps  
**Models**: 44+ Database Models  
**API Style**: REST with DRF Generic Views

---

## 📋 Project Overview

This document provides the complete folder structure for a Django backend project using:
- **Django REST Framework** (DRF) for API
- **Class-Based Views** (CBV) - Generic Views, ViewSets
- **Token Authentication** (JWT)
- **Celery** for async tasks
- **Redis** for caching
- **MySQL** for database

---

## 🗂️ Project Root Structure

```
PGManagementBackendDjango/
├── .env                          # Environment variables
├── .gitignore                    # Git ignore
├── requirements.txt              # Python dependencies
├── manage.py                     # Django CLI
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Container build
├── README.md                     # Project documentation
├── pytest.ini                    # Test configuration
├── .coveragerc                   # Test coverage config
│
├── pgmanagement/                 # Main Django project folder
│   ├── __init__.py
│   ├── settings/                 # Split settings by environment
│   │   ├── __init__.py
│   │   ├── base.py              # Common settings
│   │   ├── development.py       # Dev settings
│   │   ├── production.py        # Prod settings
│   │   └── testing.py           # Test settings
│   ├── urls.py                  # Root URL router
│   ├── wsgi.py                  # WSGI server entry
│   ├── asgi.py                  # ASGI server (WebSockets)
│   └── celery.py                # Celery configuration
│
├── apps/                         # All Django applications
│   ├── __init__.py
│   ├── users/                   # [1] Authentication & User Management
│   ├── properties/              # [2] Property, Room, Bed Management
│   ├── bookings/                # [3] Booking & Agreements
│   ├── finance/                 # [4] Invoices, Payments, Wallet
│   ├── operations/              # [5] Complaints, Safety, Entry
│   ├── mess/                    # [6] Mess Menu & Meals
│   ├── crm/                     # [7] Leads & Enquiries
│   ├── notifications/           # [8] Notifications & Templates
│   ├── visitors/                # [9] Visitor Management
│   ├── inventory/               # [10] Inventory & Stock
│   ├── payroll/                 # [11] Staff Payroll
│   ├── hygiene/                 # [12] Hygiene Inspections
│   ├── feedback/                # [13] Feedback & Ratings
│   ├── audit/                   # [14] Activity Logs
│   ├── alumni/                  # [15] Alumni Network
│   ├── saas/                    # [16] SaaS Subscriptions
│   ├── reports/                 # [17] Reports & Analytics
│   └── localization/            # [18] Multi-Language
│
├── shared/                       # Shared utilities across apps
│   ├── __init__.py
│   ├── permissions.py           # Global DRF permissions
│   ├── pagination.py            # Custom pagination
│   ├── filters.py               # Common filter classes
│   ├── exceptions.py            # Custom exceptions
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── logging_middleware.py
│   │   └── language_middleware.py
│   ├── utils/                   # Helper utilities
│   │   ├── __init__.py
│   │   ├── api_response.py     # Standard API response wrapper
│   │   ├── file_upload.py      # S3/Media upload helper
│   │   ├── pdf_generator.py    # PDF generation (invoices, agreements)
│   │   ├── sms_utils.py        # SMS/WhatsApp integration
│   │   ├── email_utils.py      # Email sending
│   │   ├── validators.py       # Custom field validators
│   │   └── helpers.py          # Generic helper functions
│   └── mixins/                  # Reusable view mixins
│       ├── __init__.py
│       ├── property_mixin.py   # Property filtering mixin
│       └── permission_mixin.py # Permission check mixin
│
├── static/                       # Static files (CSS, JS, Images)
│   └── admin/                   # Django admin customization
│
├── media/                        # User uploaded files
│   ├── profiles/                # Profile photos
│   ├── agreements/              # Digital agreements
│   ├── complaints/              # Complaint images
│   ├── assets/                  # Asset photos
│   └── invoices/                # Generated invoices
│
├── logs/                         # Application logs
│   ├── django.log
│   ├── celery.log
│   └── error.log
│
└── tests/                        # Integration tests
    ├── __init__.py
    ├── conftest.py              # Pytest fixtures
    └── integration/             # End-to-end tests
```

---

## 📦 Standard Django App Structure (with Class-Based Views)

Each Django app follows this structure:

```
apps/<app_name>/
├── __init__.py
├── models/                       # Database models (split by entity)
│   ├── __init__.py
│   └── <model_name>.py
├── serializers/                  # DRF Serializers
│   ├── __init__.py
│   ├── <model>_serializer.py    # Model serializers
│   └── custom_serializers.py    # Custom/nested serializers
├── views/                        # Class-Based Views
│   ├── __init__.py
│   ├── <model>_views.py         # ViewSets/Generic Views
│   └── custom_views.py          # Special endpoints
├── services/                     # Business logic layer
│   ├── __init__.py
│   └── <business_logic>.py      # Service classes
├── tasks.py                      # Celery async tasks
├── permissions.py                # App-specific permissions
├── filters.py                    # DRF filter classes
├── pagination.py                 # Custom pagination (if needed)
├── urls.py                       # URL routing
├── apps.py                       # App configuration
├── admin.py                      # Django admin registration
├── signals.py                    # Django signals
├── managers.py                   # Custom model managers
├──constants.py                  # App constants/enums
└── tests/                        # Unit tests
    ├── __init__.py
    ├── test_models.py
    ├── test_serializers.py
    ├── test_views.py
    └── test_services.py
```

---

## 🔐 App 1: `apps/users/` - Authentication & User Management

**Models**: CustomUser, TenantProfile, StaffProfile, OwnerProfile, ParentStudentMapping, ActivityLog

```
apps/users/
├── models/
│   ├── __init__.py
│   ├── custom_user.py           # CustomUser (AbstractUser + role field)
│   ├── tenant_profile.py        # TenantProfile (Aadhaar, credit score, preferences)
│   ├── staff_profile.py         # StaffProfile (salary, role)
│   ├── owner_profile.py         # OwnerProfile (business details, GST)
│   ├── parent_student_mapping.py # ParentStudentMapping
│   └── activity_log.py          # ActivityLog (audit trail)
├── serializers/
│   ├── __init__.py
│   ├── user_serializer.py       # UserSerializer, UserRegistrationSerializer
│   ├── tenant_serializer.py     # TenantProfileSerializer
│   ├── staff_serializer.py      # StaffProfileSerializer
│   ├── owner_serializer.py      # OwnerProfileSerializer
│   ├── auth_serializers.py      # LoginSerializer, RegisterSerializer, OTPSerializer
│   └── activity_log_serializer.py # ActivityLogSerializer
├── views/
│   ├── __init__.py
│   ├── auth_views.py            # LoginView, RegisterView, OTPVerifyView (APIView)
│   ├── user_views.py            # UserViewSet (ModelViewSet)
│   ├── tenant_views.py          # TenantProfileViewSet
│   ├── staff_views.py           # StaffProfileViewSet
│   ├── owner_views.py           # OwnerProfileViewSet
│   ├── profile_views.py         # UserProfileView, UpdateProfileView
│   └── activity_log_views.py   # ActivityLogViewSet (read-only)
├── services/
│   ├── __init__.py
│   ├── auth_service.py          # handle_otp_send(), verify_otp(), generate_jwt()
│   ├── user_service.py          # create_user(), update_profile()
│   └── activity_logger.py       # log_activity(user, action, details)
├── tasks.py                      # send_welcome_email.delay()
├── permissions.py                # IsOwnerOrReadOnly, IsStaffUser
├── filters.py                    # UserFilter, TenantFilter
├── urls.py                       # /api/v1/auth/*, /api/v1/users/*
├── admin.py
├── signals.py                    # post_save signal for profile creation
└── tests/
    ├── test_auth.py
    ├── test_user_model.py
    └── test_permissions.py
```

**Key Class-Based Views:**
- `LoginView(APIView)` - POST /auth/login/
- `RegisterView(APIView)` - POST /auth/register/
- `UserViewSet(ModelViewSet)` - CRUD for users
- `TenantProfileViewSet(ModelViewSet)` - Tenant management
- `ActivityLogViewSet(ReadOnlyModelViewSet)` - Audit logs

---

## 🏢 App 2: `apps/properties/` - Property Management

**Models**: Property, Room, Bed, PricingRule, Asset, AssetServiceLog, ElectricityReading

```
apps/properties/
├── models/
│   ├── property.py              # Property (name, address, owner)
│   ├── room.py                  # Room (number, type, capacity, rent)
│   ├── bed.py                   # Bed (label, is_occupied, iot_meter_id)
│   ├── pricing_rule.py          # PricingRule (dynamic pricing)
│   ├── asset.py                 # Asset (AC, geyser, furniture)
│   ├── asset_service_log.py     # AssetServiceLog (maintenance history)
│   └── electricity_reading.py   # ElectricityReading (IoT meter data)
├── serializers/
│   ├── property_serializer.py   # PropertySerializer, PropertyListSerializer
│   ├── room_serializer.py       # RoomSerializer, RoomDetailSerializer
│   ├── bed_serializer.py        # BedSerializer, BedAvailabilitySerializer
│   ├── pricing_serializer.py    # PricingRuleSerializer
│   ├── asset_serializer.py      # AssetSerializer, AssetServiceLogSerializer
│   └── electricity_serializer.py # ElectricityReadingSerializer
├── views/
│   ├── property_views.py        # PropertyViewSet (ModelViewSet)
│   ├── room_views.py            # RoomViewSet, CheckAvailabilityView
│   ├── bed_views.py             # BedViewSet, BedOccupancyView
│   ├── pricing_views.py         # PricingRuleViewSet
│   ├── asset_views.py           # AssetViewSet, AssetServiceLogViewSet
│   └── electricity_views.py     # ElectricityReadingViewSet, MonthlyConsumptionView
├── services/
│   ├── dynamic_pricing.py       # calculate_rent(room, date)
│   ├── availability_checker.py  # check_bed_availability(property, dates)
│   ├── iot_integration.py       # fetch_meter_reading(bed_id)
│   └── asset_maintenance.py     # schedule_maintenance(asset)
├── tasks.py                      # sync_iot_readings.delay(), check_warranty.delay()
├── permissions.py                # IsPropertyOwnerOrManager
├── filters.py                    # PropertyFilter, RoomFilter, BedFilter
├── urls.py                       # /api/v1/properties/*
└── tests/
```

**Key Class-Based Views:**
- `PropertyViewSet(ModelViewSet)` - Property CRUD
- `RoomViewSet(ModelViewSet)` - Room management
- `BedViewSet(ModelViewSet)` - Bed management
- `CheckAvailabilityView(APIView)` - Check bed availability
- `BedOccupancyView(APIView)` - GET occupancy statistics

---

## 📅 App 3: `apps/bookings/` - Booking Management

**Models**: Booking, DigitalAgreement, RoomChangeHistory

```
apps/bookings/
├── models/
│   ├── booking.py               # Booking (tenant, bed, dates, status, rent)
│   ├── digital_agreement.py     # DigitalAgreement (PDF, signatures)
│   └── room_change_history.py   # RoomChangeHistory (internal transfers)
├── serializers/
│   ├── booking_serializer.py    # BookingSerializer, BookingCreateSerializer
│   ├── agreement_serializer.py  # DigitalAgreementSerializer
│   └── room_change_serializer.py # RoomChangeHistorySerializer
├── views/
│   ├── booking_views.py         # BookingViewSet (ModelViewSet)
│   ├── agreement_views.py       # DigitalAgreementViewSet, SignAgreementView
│   ├── room_change_views.py     # RoomChangeRequestView, ApproveRoomChangeView
│   └── checkout_views.py        # CheckoutView (tenant exit process)
├── services/
│   ├── booking_service.py       # create_booking(), calculate_deposit()
│   ├── agreement_generator.py   # generate_agreement_pdf(booking)
│   ├── room_change_service.py   # process_room_change(request)
│   └── checkout_service.py      # process_checkout(booking), calculate_refund()
├── tasks.py                      # send_agreement_email.delay(), process_checkout.delay()
├── permissions.py                # IsBookingOwnerOrManager
├── filters.py                    # BookingFilter (by status, property, tenant)
├── urls.py                       # /api/v1/bookings/*
└── tests/
```

**Key Class-Based Views:**
- `BookingViewSet(ModelViewSet)` - Booking CRUD
- `DigitalAgreementViewSet(ReadOnlyModelViewSet)` - View agreements
- `SignAgreementView(APIView)` - POST /bookings/{id}/sign/
- `RoomChangeRequestView(APIView)` - POST /bookings/room-change/
- `CheckoutView(APIView)` - POST /bookings/{id}/checkout/

---

## 💰 App 4: `apps/finance/` - Financial Management

**Models**: Invoice, Payment, Expense, RefundTransaction

```
apps/finance/
├── models/
│   ├── invoice.py               # Invoice (monthly bills)
│   ├── payment.py               # Payment (transactions)
│   ├── expense.py               # Expense (operational costs)
│   └── refund_transaction.py    # RefundTransaction (deposit refunds)
├── serializers/
│   ├── invoice_serializer.py    # InvoiceSerializer, InvoiceDetailSerializer
│   ├── payment_serializer.py    # PaymentSerializer, PaymentCreateSerializer
│   ├── expense_serializer.py    # ExpenseSerializer
│   └── refund_serializer.py     # RefundTransactionSerializer
├── views/
│   ├── invoice_views.py         # InvoiceViewSet, GenerateInvoiceView
│   ├── payment_views.py         # PaymentViewSet, ProcessPaymentView, PaymentCallbackView
│   ├── expense_views.py         # ExpenseViewSet
│   ├── refund_views.py          # RefundTransactionViewSet, ProcessRefundView
│   └── wallet_views.py          # WalletBalanceView, WalletRechargeView, WalletHistoryView
├── services/
│   ├── invoice_generator.py     # generate_monthly_invoices()
│   ├── payment_processor.py     # process_payment(), verify_payment()
│   ├── wallet_manager.py        # deduct_from_wallet(), add_to_wallet()
│   ├── refund_calculator.py     # calculate_refund_amount(booking)
│   └── payment_gateway.py       # integrate with Razorpay/Stripe
├── tasks.py                      # generate_monthly_invoices.delay(), send_payment_reminder.delay()
├── permissions.py                # IsOwnerOrManager, IsInvoiceOwner
├── filters.py                    # InvoiceFilter, PaymentFilter, ExpenseFilter
├── urls.py                       # /api/v1/finance/*
└── tests/
```

**Key Class-Based Views:**
- `InvoiceViewSet(ModelViewSet)` - Invoice management
- `GenerateInvoiceView(APIView)` - POST /finance/invoices/generate/
- `PaymentViewSet(ModelViewSet)` - Payment history
- `ProcessPaymentView(APIView)` - POST /finance/payments/process/
- `WalletRechargeView(APIView)` - POST /finance/wallet/recharge/

---

## 🛠️ App 5: `apps/operations/` - Operations & Safety

**Models**: Complaint, EmergencyAlert, EntryLog, Notice, ChatLog, GeofenceSettings, VideoCallLog

```
apps/operations/
├── models/
│   ├── complaint.py             # Complaint (tenant issues)
│   ├── emergency_alert.py       # EmergencyAlert (SOS button)
│   ├── entry_log.py             # EntryLog (biometric/QR entry)
│   ├── notice.py                # Notice (announcements)
│   ├── chat_log.py              # ChatLog (AI chatbot)
│   ├── geofence_settings.py     # GeofenceSettings (parent safe zones)
│   └── video_call_log.py        # VideoCallLog (parent-manager calls)
├── serializers/
│   ├── complaint_serializer.py  # ComplaintSerializer, ComplaintCreateSerializer
│   ├── emergency_serializer.py  # EmergencyAlertSerializer
│   ├── entry_log_serializer.py  # EntryLogSerializer
│   ├── notice_serializer.py     # NoticeSerializer
│   ├── chat_log_serializer.py   # ChatLogSerializer
│   ├── geofence_serializer.py   # GeofenceSettingsSerializer
│   └── video_call_serializer.py # VideoCallLogSerializer
├── views/
│   ├── complaint_views.py       # ComplaintViewSet, AssignComplaintView, ResolveComplaintView
│   ├── emergency_views.py       # EmergencyAlertViewSet, TriggerSOSView, ResolveSOSView
│   ├── entry_log_views.py       # EntryLogViewSet, RecordEntryView
│   ├── notice_views.py          # NoticeViewSet (with permissions)
│   ├── chat_views.py            # ChatBotView (APIView for bot interaction)
│   ├── geofence_views.py        # GeofenceSettingsViewSet
│   └── video_call_views.py      # VideoCallLogViewSet, InitiateCallView
├── services/
│   ├── complaint_handler.py     # assign_complaint(), auto_escalate()
│   ├── emergency_handler.py     # trigger_sos(), notify_all()
│   ├── chatbot_logic.py         # process_message(), detect_intent()
│   ├── entry_validator.py       # validate_entry(), check_late_entry()
│   └── geofence_monitor.py      # check_zone_exit(), send_alert()
├── tasks.py                      # send_sos_alerts.delay(), check_geofence.delay()
├── permissions.py                # IsComplaintOwner, IsManagerOrOwner
├── filters.py                    # ComplaintFilter, EntryLogFilter
├── urls.py                       # /api/v1/operations/*
└── tests/
```

**Key Class-Based Views:**
- `ComplaintViewSet(ModelViewSet)` - Complaint management
- `TriggerSOSView(APIView)` - POST /operations/emergency/trigger/
- `RecordEntryView(APIView)` - POST /operations/entry/record/
- `ChatBotView(APIView)` - POST /operations/chat/
- `GeofenceSettingsViewSet(ModelViewSet)` - Geofence management

---

## 🍛 App 6: `apps/mess/` - Mess Management

**Models**: MessMenu, DailyMealSelection, MessFeedback

```
apps/mess/
├── models/
│   ├── mess_menu.py             # MessMenu (daily menu)
│   ├── daily_meal_selection.py  # DailyMealSelection (tenant choices)
│   └── mess_feedback.py         # MessFeedback (food ratings)
├── serializers/
│   ├── menu_serializer.py       # MessMenuSerializer
│   ├── meal_selection_serializer.py # DailyMealSelectionSerializer
│   └── feedback_serializer.py   # MessFeedbackSerializer
├── views/
│   ├── menu_views.py            # MessMenuViewSet
│   ├── meal_selection_views.py  # DailyMealSelectionViewSet, MarkMealView
│   └── feedback_views.py        # MessFeedbackViewSet
├── services/
│   ├── meal_billing.py          # calculate_daily_cost(), deduct_from_wallet()
│   ├── menu_planner.py          # suggest_menu()
│   └── feedback_analyzer.py     # analyze_ratings()
├── tasks.py                      # process_daily_billing.delay()
├── permissions.py                # IsTenantOrManager
├── filters.py                    # MenuFilter, MealSelectionFilter
├── urls.py                       # /api/v1/mess/*
└── tests/
```

**Key Class-Based Views:**
- `MessMenuViewSet(ModelViewSet)` - Menu management
- `DailyMealSelectionViewSet(ModelViewSet)` - Meal choices
- `MarkMealView(APIView)` - POST /mess/meals/mark/ (eating/skipping)
- `MessFeedbackViewSet(ModelViewSet)` - Food ratings

---

## 🤝 App 7: `apps/crm/` - CRM & Leads

**Models**: Lead

```
apps/crm/
├── models.py                    # Lead (enquiries)
├── serializers/
│   └── lead_serializer.py       # LeadSerializer, LeadCreateSerializer
├── views/
│   ├── lead_views.py            # LeadViewSet (ModelViewSet)
│   └── conversion_views.py      # ConvertLeadView (APIView)
├── services/
│   ├── lead_manager.py          # assign_lead(), convert_to_tenant()
│   └── lead_scorer.py           # calculate_lead_score()
├── tasks.py                      # send_follow_up.delay()
├── permissions.py                # IsManagerOrOwner
├── filters.py                    # LeadFilter (by status, source)
├── urls.py                       # /api/v1/crm/*
└── tests/
```

---

## 🔔 App 8: `apps/notifications/` - Notifications

**Models**: Notification, FCMToken, MessageTemplate

```
apps/notifications/
├── models/
│   ├── notification.py          # Notification (logs)
│   ├── fcm_token.py             # FCMToken (device tokens)
│   └── message_template.py      # MessageTemplate (templates)
├── serializers/
│   ├── notification_serializer.py # NotificationSerializer
│   ├── fcm_token_serializer.py  # FCMTokenSerializer
│   └── template_serializer.py   # MessageTemplateSerializer
├── views/
│   ├── notification_views.py    # NotificationViewSet, MarkAsReadView
│   ├── fcm_token_views.py       # FCMTokenViewSet, RegisterDeviceView
│   └── template_views.py        # MessageTemplateViewSet
├── services/
│   ├── notification_dispatcher.py # send_notification(), send_bulk()
│   ├── fcm_handler.py           # send_push_notification()
│   ├── sms_handler.py           # send_sms()
│   ├── email_handler.py         # send_email()
│   └── template_renderer.py     # render_template(template, context)
├── tasks.py                      # send_bulk_notifications.delay()
├── permissions.py                # IsNotificationRecipient
├── filters.py                    # NotificationFilter
├── urls.py                       # /api/v1/notifications/*
└── tests/
```

---

## 🚪 App 9-18: Simplified Structure

For brevity, here's the simplified structure for remaining apps:

### App 9: `apps/visitors/`
- Models: VisitorRequest
- Views: VisitorRequestViewSet, ApproveVisitorView
- Services: visitor_manager.py

### App 10: `apps/inventory/`
- Models: InventoryItem, InventoryTransaction
- Views: InventoryItemViewSet, InventoryTransactionViewSet
- Services: stock_manager.py

### App 11: `apps/payroll/`
- Models: StaffAttendance, SalaryPayment
- Views: StaffAttendanceViewSet, SalaryPaymentViewSet
- Services: salary_calculator.py

### App 12: `apps/hygiene/`
- Models: HygieneInspection
- Views: HygieneInspectionViewSet
- Services: hygiene_scorer.py

### App 13: `apps/feedback/`
- Models: ComplaintFeedback, MessFeedback
- Views: ComplaintFeedbackViewSet, MessFeedbackViewSet

### App 14: `apps/audit/`
- Models: AuditLog
- Views: AuditLogViewSet (ReadOnly)
- Middleware: audit_middleware.py

### App 15: `apps/alumni/`
- Models: AlumniProfile, JobReferral
- Views: AlumniProfileViewSet, JobReferralViewSet

### App 16: `apps/saas/`
- Models: SubscriptionPlan, SaasSubscription, AppVersion
- Views: SubscriptionPlanViewSet, SaasSubscriptionViewSet

### App 17: `apps/reports/`
- Models: GeneratedReport
- Views: GenerateReportView, DownloadReportView
- Services: report_generator.py, excel_exporter.py

### App 18: `apps/localization/`
- Models: TranslationString
- Views: TranslationStringViewSet, GetTranslationsView
- Services: translation_manager.py

---

## 🎯 Summary

**Total Structure:**
- 18 Django Apps
- 44+ Models
- 100+ Class-Based Views
- RESTful API endpoints
- Complete test coverage
- Production-ready architecture

**Next Steps:**
1. Create apps: `python manage.py startapp <app_name>`
2. Implement models from All_Database_Tables_Models.md
3. Create serializers for each model
4. Implement class-based views (ViewSets, APIViews)
5. Write business logic in services/
6. Add tests for each component
7. Configure URLs and deploy

---

**✅ Documentation Version:** 3.0 (Class-Based Views)  
**📅 Last Updated:** January 2026  
**🎯 Apps:** 18 Django Apps  
**🎯 Models:** 44+ Database Models  
**🎯 Views:** Class-Based (DRF)