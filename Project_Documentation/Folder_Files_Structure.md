# 🏨 Smart PG Management System - Complete Folder Structure (Modular Monolith)

Ye documentation **Smart PG Management System** ka detailed folder structure hai. Har file ka purpose, content, aur responsibility clearly explain ki gayi hai taaki new developers ko samajh aaye ki kya kahan hoga aur kaise kaam karega.

**Architecture Style**: Modular Monolith (18 Independent Feature Apps)

## Related Documentation
- **Service Architecture**: All_Services_Documentation.md (Service details, business logic)
- **Database Models**: All_Database_Tables_Models.md (All 40+ Django models)
- **Database Details**: Database_Table_Fields_Description.md (Field descriptions, constraints)
- **Feature Summary**: Project_Summary_Features.md (High-level overview with 15 USPs)

---

## Django Project Root Structure

```text
/PGManagementBackendDjango/     // Project Root
│
├── .env                        // Global environment variables (DATABASE_URL, JWT_SECRET, REDIS_URL)
├── .gitignore                  // Git ignore file
├── requirements.txt            // All Python dependencies
├── manage.py                   // Django management script
├── docker-compose.yml          // Docker setup (Django + MySQL + Redis + Celery)
├── Dockerfile                  // Docker build config
├── README.md                   // Project overview & setup
│
├── core/                       // Project Core (Settings & Config)
│   ├── __init__.py
│   ├── settings.py             // Django settings (Apps, Middleware, DB, All configs)
│   ├── urls.py                 // Main URL Router (Includes all app URLs)
│   ├── wsgi.py                 // WSGI (Sync)
│   └── asgi.py                 // ASGI (Async for WebSockets)
│
├── shared/                     // Shared Utilities (Used across multiple apps)
│   ├── __init__.py
│   ├── middleware/             // Global Middleware
│   │   ├── error_handling.py
│   │   ├── request_logging.py
│   │   └── cors_middleware.py
│   ├── utils/                  // Helper Functions
│   │   ├── api_response.py     // Standardized API Response Wrapper
│   │   ├── file_upload.py      // S3 Upload Logic
│   │   ├── pdf_generator.py    // PDF Invoice/Agreement Gen
│   │   ├── sms_utils.py        // SMS/Whatsapp Sending Utils
│   │   └── translation.py      // Language Translation Helpers
│   ├── permissions.py          // Global Permissions (IsSuperAdmin, IsManager)
│   └── localization/           // Multi-Language Support
│       ├── middleware.py       // Language Detection Middleware
│       └── language_loader.py  // Load translations from DB
│
├── apps/                       // The 18 Logic Modules (Feature Apps)
│   ├── users/                  // [App 1] Auth, Roles, Profiles
│   ├── properties/             // [App 2] Property, Rooms, Beds, Assets
│   ├── bookings/               // [App 3] Bookings, Agreements, Exits
│   ├── finance/                // [App 4] Invoices, Wallet, Expenses
│   ├── operations/             // [App 5] Complaints, EntryLogs, Notices
│   ├── mess/                   // [App 6] Menu, Daily Meals, Payments
│   ├── crm/                    // [App 7] Leads, Enquiries
│   ├── notifications/          // [App 8] Logs, FCM Tokens
│   ├── visitors/               // [App 9] Visitor Management
│   ├── inventory/              // [App 10] Kitchen Stock
│   ├── payroll/                // [App 11] Staff Attendance & Salary
│   ├── hygiene/                // [App 12] Inspections
│   ├── feedback/               // [App 13] Ratings
│   ├── audit/                  // [App 14] Activity Logs
│   ├── alumni/                 // [App 15] Alumni Network
│   ├── saas/                   // [App 16] Subscription Plans
│   ├── reports/                // [App 17] Analytics & Export
│   └── localization/           // [App 18] Multi-Language Support
│
├── media/                      // User Uploaded Files (Local Dev)
└── static/                     // Static Assets
```

---

## 📂 Detailed App Structure (Inside `apps/`)

Modules ko standard structure follow karna chahiye:

### 1. `apps/users` (Identity)
Handles Login, Registration, and Profiles.
```text
apps/users/
├── models/
│   ├── user.py                 # CustomUser (AbstractUser)
│   ├── tenant_profile.py       # TenantProfile (Aadhaar, Guardian)
│   └── staff_profile.py        # StaffProfile (Role, Salary)
├── serializers/                # DRF Serializers
├── views/                      # API Controllers
├── services/                   # Business Logic (Register, Verify)
├── urls.py                     # /api/v1/auth/*
└── tests/
```

### 2. `apps/properties` (Inventory - Rooms)
Handles Buildings, Rooms, Beds, Utilities, IoT.
```text
apps/properties/
├── models/
│   ├── property.py             # Property (Branch)
│   ├── room.py                 # Room (Capacity, Rent)
│   ├── bed.py                  # Bed (IoT ID, Vacancy)
│   ├── asset.py                # Asset (AC, Geyser)
│   └── pricing.py              # PricingRule (Dynamic Rent)
├── services/
│   ├── dynamic_pricing.py      # Logic for rent calculation
│   └── iot_integration.py      # Reading meter data
└── urls.py                     # /api/v1/properties/*
```

### 3. `apps/bookings` (Transactions)
Handles Booking Lifecycle, Agreements.
```text
apps/bookings/
├── models/
│   ├── booking.py              # Booking (Dates, Status)
│   └── agreement.py            # DigitalAgreement (PDF)
├── services/
│   ├── allocation.py           # Room Allocation Logic
│   └── agreement_gen.py        # Generate PDF Agreement
└── urls.py                     # /api/v1/bookings/*
```

### 4. `apps/finance` (Money)
Handles Invoices, Wallet, Expenses.
```text
apps/finance/
├── models/
│   ├── invoice.py              # Monthly Bill
│   ├── transaction.py          # Ledger (Credit/Debit)
│   └── expense.py              # Property Expenses
├── services/
│   ├── invoice_generator.py    # Cron Job Logic
│   └── wallet_manager.py       # Deduct/Add Money
└── urls.py                     # /api/v1/finance/*
```

### 5. `apps/operations` (Day-to-Day)
Handles Complaints, Safety, Chatbot.
```text
apps/operations/
├── models/
│   ├── complaint.py            # Complaints
│   ├── entry_log.py            # Biometric Logs
│   ├── notice.py               # Notice Board
│   └── chat_log.py             # AI Bot History
├── services/
│   ├── chatbot_logic.py        # NLP/Regex for Bot
│   └── complaint_router.py     # Assign to Manager
└── urls.py                     # /api/v1/operations/*
```

### 6. `apps/mess` (Food)
Handles Food Menu & Daily Selection.
```text
apps/mess/
├── models/
│   ├── menu.py                 # Daily Menu
│   └── selection.py            # Tenant Choice (Eating/Skipping)
├── services/
│   └── meal_billing.py         # Calc daily cost
└── urls.py                     # /api/v1/mess/*
```

### 7. `apps/crm` (Sales)
Handles Leads & Enquiries.
```text
apps/crm/
├── models.py                   # Lead (Status: New/Converted)
├── serializers.py
├── views.py
└── urls.py                     # /api/v1/crm/*
```

### 8. `apps/notifications` (Communication)
Handles User Alerts.
```text
apps/notifications/
├── models.py                   # NotificationLog, FCMToken
├── services/
│   └── dispatcher.py           # Send SMS/Email/Push
└── urls.py
```

### 9. `apps/visitors` (Security)
Handles Gate Approvals.
```text
apps/visitors/
├── models.py                   # VisitorRequest
├── views.py                    # Approve/Reject endpoints
└── urls.py
```

### 10. `apps/inventory` (Stock)
Handles Kitchen/Housekeeping Stock (Groceries).
```text
apps/inventory/
├── models.py                   # InventoryItem, InventoryTransaction
├── views.py
└── urls.py
```
*(Note: Do not confuse with 'properties'. This is consummable stock like Rice/Oil)*

### 11. `apps/payroll` (HR)
Handles Staff.
```text
apps/payroll/
├── models.py                   # StaffAttendance, SalaryPayment
├── services/
│   └── salary_calc.py          # Calculate based on attendance
└── urls.py
```

### 12. `apps/hygiene` (Quality)
Checks & Scores.
```text
apps/hygiene/
├── models.py                   # HygieneInspection
├── views.py
└── urls.py
```

### 13. `apps/feedback` (Reviews)
Tenant Feedback.
```text
apps/feedback/
├── models.py                   # ComplaintFeedback, MessFeedback
└── urls.py
```

### 14. `apps/audit` (Logs) - *Technical*
Tracks who did what.
```text
apps/audit/
├── models.py                   # AuditLog (User, Action, Timestamp)
└── middleware/
    └── audit_middleware.py     # Auto-log requests
```

### 15. `apps/alumni` (Community)
Ex-students.
```text
apps/alumni/
├── models.py                   # AlumniProfile, JobPost
└── urls.py
```

### 16. `apps/saas` (SuperAdmin)
Subscription & Tenant Management (If selling software).
```text
apps/saas/
├── models.py                   # SubscriptionPlan, TenantLicense
└── urls.py
```

### 17. `apps/reports` (Analytics)
Data Dump.
```text
apps/reports/
├── services/
│   ├── excel_export.py         # Generate .xlsx
│   └── chart_data.py           # Aggregation logic
└── views.py                    # Download endpoints
```

### 18. `apps/localization` (Multi-Language) - *NEW*
Handles translations for 6 languages.
```text
apps/localization/
├── models.py                   # TranslationString (module, key, language, value)
├── serializers.py
├── views.py                    # Get/Set translations
├── services/
│   ├── translation_manager.py  # CRUD operations for translations
│   └── language_detector.py    # Detect user language from request
├── management/
│   └── commands/
│       └── load_translations.py # Import bulk translations from JSON/CSV
└── urls.py                     # /api/v1/localization/*
```

**Supported Languages**:
- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Bengali (bn)

**Key Features**:
- Dynamic UI string loading based on user's `preferred_language`
- Admin interface for managing translations
- Fallback to English if translation missing
- Translation caching for performance

---

---

## 🛠️ Infrastructure & Config

### `core/settings.py`
- **Single Settings File**: Contains all configurations
- **Installed Apps**: All 18 Django apps registered
- **Database**: SQLite (development) / MySQL (production)
- **Custom User Model**: `AUTH_USER_MODEL = 'users.CustomUser'`
- **REST Framework**: API configuration
- **Multi-language**: 6 languages supported

### `docker-compose.yml`
- **web**: Django Gunicorn
- **db**: MySQL 8.0
- **redis**: Redis 7 (Caching/Celery)
- **worker**: Celery Worker (Async Tasks)
- **beat**: Celery Beat (Cron Jobs like Monthly Invoice)

---

## ✅ Summary of Changes (Version 2.0)

Is documentation ko update kiya gaya hai to reflect:

1. **ALL 18 Apps** (Latest: Added Localization app for multi-language support)
2. **40+ Models** (Updated from 39+, includes TranslationString model)
3. **Correct App Names**: 
   - `bookings` (formerly tenants) for consistency
   - `properties` for Rooms/Beds/Assets
   - `inventory` for Kitchen Stock
   - `localization` for Multi-Language Support
4. **Full ERP Scope**: Audit, SaaS, Reports, Alumni, and Localization apps
5. **Multi-Language Infrastructure**: 
   - Translation middleware in shared/localization/
   - Language utilities for 6 languages (en, hi, ta, te, kn, bn)
   - User preference based UI rendering

### Alignment Status: 100% ✅

Ye structure ab completely aligned hai with:
- ✅ `Project_Summary_Features.md` - All 33 features supported
- ✅ `All_Services_Documentation.md` - All 18 apps documented
- ✅ `All_Database_Tables_Models.md` - All 40+ models included
- ✅ `Database_Table_Fields_Description.md` - Field-level details match

### Key Highlights:

- **Modular Monolith Architecture**: 18 independent Django apps with clear boundaries
- **Scalable Structure**: Easy to convert to microservices later if needed
- **Complete Feature Coverage**: 15 USP Features + 9 Advanced Features + 9 Technical Features
- **Production Ready**: Includes Docker, Celery, Redis, Multi-language support
- **Beginner Friendly**: Clear folder structure with purpose-driven organization

**Next Steps**: 
1. Create Django apps using `python manage.py startapp <app_name>`
2. Implement models from All_Database_Tables_Models.md
3. Build services and views following this structure
4. Deploy with Docker Compose

---

**📝 Document Version:** 2.0 (Complete & Fully Aligned)  
**📅 Last Updated:** December 2025  
**🎯 Total Apps:** 18 Django apps  
**🎯 Total Models:** 40+ database models  
**✅ Feature Coverage:** 33/33 Features (100%)