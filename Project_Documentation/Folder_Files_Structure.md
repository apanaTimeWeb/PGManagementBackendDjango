# 🏨 Smart PG Management System - Complete Folder Structure (Modular Monolith)

Ye documentation **Smart PG Management System** ka detailed folder structure hai. Har file ka purpose, content, aur responsibility clearly explain ki gayi hai taaki new developers ko samajh aaye ki kya kahan hoga aur kaise kaam karega.

## Related Documentation
- **Service Architecture**: All_Services_Documentation.md (Service details, business logic)
- **Database Models**: All_Database_Tables_Models.md (All 12 Django models)
- **Database Details**: Database_Table_Fields_Description.md (Field descriptions, constraints)
- **Feature Summary**: Project_Summary_Features.md (High-level overview with 15 USPs)

---

## Django Project Root Structure

```
/smart_pg_backend/
│
├── .env                            // Global environment variables (DATABASE_URL, JWT_SECRET, REDIS_URL)
├── .gitignore                      // Git ignore file for __pycache__, .env files, media, logs
├── requirements.txt                // All Python dependencies (Django, DRF, PostgreSQL, Redis, Celery)
├── manage.py                       // Django management script
├── docker-compose.yml              // Docker setup for Django + PostgreSQL + Redis
├── Dockerfile                      // Docker container configuration
├── README.md                       // Project overview, setup instructions, API documentation links
│
├── core/                           // Django project settings and global configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 // Base settings (common configurations)
│   │   ├── development.py          // Development environment settings
│   │   ├── production.py           // Production environment settings
│   │   └── testing.py              // Test environment settings
│   ├── urls.py                     // Main URL routing for all apps
│   ├── wsgi.py                     // WSGI configuration for deployment
│   └── asgi.py                     // ASGI configuration for async features
│
├── shared/                         // Shared utilities across all apps
│   ├── __init__.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py      // JWT token validation middleware (reusable)
│   │   ├── cors_middleware.py      // CORS configuration for all apps
│   │   └── rate_limit_middleware.py // Rate limiting configuration
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_response.py         // Standardized API response format
│   │   ├── logger.py               // Django logger configuration
│   │   ├── validation.py           // Common validation functions
│   │   └── encryption.py           // Password hashing and JWT utilities
│   └── constants/
│       ├── __init__.py
│       ├── http_status.py          // HTTP status codes
│       ├── messages.py             // Common success/error messages
│       └── permissions.py          // Permission constants for all apps
│
├── apps/                           // All 6 Django apps (Modular Monolith)
│   │
│   ├── users/                      // App 1: User Management & Authentication (USP 1, 2, 10, 11)
│   │   ├── __init__.py
│   │   ├── apps.py                 // App configuration
│   │   ├── admin.py                // Django admin interface customization
│   │   ├── migrations/             // Database migration files
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py     // Initial migration for CustomUser, TenantProfile
│   │   │   └── ...
│   │   │
│   │   ├── models/                 // Database models (2 models)
│   │   │   ├── __init__.py         // Import all models
│   │   │   ├── user.py             // CustomUser model with roles, SOS contact
│   │   │   └── tenant_profile.py   // TenantProfile model with wallet, Aadhaar, credit score
│   │   │
│   │   ├── serializers/            // DRF serializers for API responses
│   │   │   ├── __init__.py
│   │   │   ├── auth_serializers.py // Registration, login, password reset serializers
│   │   │   ├── user_serializers.py // User profile, update serializers
│   │   │   └── tenant_serializers.py // Tenant profile, parent portal serializers
│   │   │
│   │   ├── views/                  // API views and business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_views.py       // Registration, login, JWT token management
│   │   │   │                       // Functions: register_user, login_user, refresh_token, forgot_password
│   │   │   ├── user_views.py       // User profile management
│   │   │   │                       // Functions: get_profile, update_profile, change_password
│   │   │   ├── parent_views.py     // Parent portal access (USP 1)
│   │   │   │                       // Functions: get_my_wards, ward_details, ward_transactions
│   │   │   ├── sos_views.py        // SOS emergency system (USP 11)
│   │   │   │                       // Functions: trigger_sos_alert, get_emergency_contacts
│   │   │   └── verification_views.py // Aadhaar upload & police verification (USP 2)
│   │   │                           // Functions: upload_aadhaar, submit_police_verification
│   │   │
│   │   ├── services/               // Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py     // Authentication business logic
│   │   │   │                       // Functions: create_user, validate_credentials, generate_tokens
│   │   │   ├── user_service.py     // User management business logic
│   │   │   │                       // Functions: get_user_by_id, update_user_profile, change_password
│   │   │   ├── parent_service.py   // Parent portal business logic
│   │   │   │                       // Functions: get_ward_details, send_parent_notifications
│   │   │   ├── sos_service.py      // SOS alert business logic
│   │   │   │                       // Functions: trigger_emergency_alert, notify_contacts
│   │   │   └── verification_service.py // Police verification business logic
│   │   │                           // Functions: process_aadhaar_upload, submit_to_police_api
│   │   │
│   │   ├── urls.py                 // App URL routing
│   │   │                           // Routes: /auth/, /profile/, /parent/, /sos/, /verification/
│   │   │
│   │   ├── permissions.py          // Custom permissions for different user roles
│   │   ├── validators.py           // Input validation for user data
│   │   └── tests/                  // Unit and integration tests
│   │       ├── __init__.py
│   │       ├── test_auth.py        // Authentication tests
│   │       ├── test_user.py        // User management tests
│   │       └── test_parent.py      // Parent portal tests
│   │
│   ├── inventory/                  // App 2: Property & Rooms Management (USP 3, 4, 5)
│   │   ├── __init__.py
│   │   ├── apps.py, admin.py, migrations/
│   │   │
│   │   ├── models/                 // Database models (2 models)
│   │   │   ├── __init__.py
│   │   │   ├── room.py             // Room model with dynamic pricing, amenities
│   │   │   └── bed.py              // Bed model with public UID, IoT meter integration
│   │   │
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── room_serializers.py // Room listing, filtering serializers
│   │   │   └── bed_serializers.py  // Bed availability, public link serializers
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── room_views.py       // Room management and listing
│   │   │   │                       // Functions: list_rooms, get_room_details, filter_rooms
│   │   │   ├── bed_views.py        // Bed management and availability
│   │   │   │                       // Functions: list_available_beds, get_bed_by_public_uid
│   │   │   ├── public_views.py     // Public bed link access (USP 3)
│   │   │   │                       // Functions: get_bed_by_public_link, check_availability
│   │   │   ├── pricing_views.py    // Dynamic pricing management (USP 4)
│   │   │   │                       // Functions: update_seasonal_pricing, get_pricing_history
│   │   │   └── iot_views.py        // IoT meter readings (USP 5)
│   │   │                           // Functions: receive_meter_reading, get_electricity_usage
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── room_service.py     // Room business logic
│   │   │   ├── bed_service.py      // Bed availability business logic
│   │   │   ├── pricing_service.py  // Dynamic pricing algorithms
│   │   │   └── iot_service.py      // IoT integration business logic
│   │   │
│   │   ├── urls.py                 // Routes: /rooms/, /beds/, /public/, /iot/
│   │   ├── permissions.py, validators.py, tests/
│   │
│   ├── bookings/                   // App 3: Tenant Lifecycle Management (USP 6, 7, 8, 9)
│   │   ├── __init__.py
│   │   ├── apps.py, admin.py, migrations/
│   │   │
│   │   ├── models/                 // Database models (1 model)
│   │   │   ├── __init__.py
│   │   │   └── booking.py          // Booking model with zero deposit, digital agreement
│   │   │
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── booking_serializers.py // Booking creation, update serializers
│   │   │   └── agreement_serializers.py // Digital agreement serializers
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── booking_views.py    // Booking management
│   │   │   │                       // Functions: create_booking, get_user_bookings, update_booking
│   │   │   ├── matching_views.py   // AI compatibility matching (USP 6)
│   │   │   │                       // Functions: find_compatible_roommates, get_matching_score
│   │   │   ├── agreement_views.py  // Digital agreement & eSign (USP 7)
│   │   │   │                       // Functions: upload_agreement, sign_digitally, get_signed_agreement
│   │   │   ├── payment_views.py    // Zero deposit & fintech integration (USP 8)
│   │   │   │                       // Functions: process_zero_deposit, integrate_fintech_loan
│   │   │   └── exit_views.py       // Digital notice & auto refund (USP 9)
│   │   │                           // Functions: request_exit, calculate_refund, process_auto_refund
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── booking_service.py  // Booking business logic
│   │   │   ├── matching_service.py // AI matching algorithms
│   │   │   ├── agreement_service.py // Digital agreement processing
│   │   │   ├── payment_service.py  // Zero deposit processing
│   │   │   └── exit_service.py     // Exit and refund calculations
│   │   │
│   │   ├── urls.py                 // Routes: /bookings/, /matching/, /agreements/, /exit/
│   │   ├── permissions.py, validators.py, tests/
│   │
│   ├── finance/                    // App 4: Finance Management (USP 10)
│   │   ├── __init__.py
│   │   ├── apps.py, admin.py, migrations/
│   │   │
│   │   ├── models/                 // Database models (2 models)
│   │   │   ├── __init__.py
│   │   │   ├── invoice.py          // Invoice model with auto-generation
│   │   │   └── wallet_transaction.py // WalletTransaction model for all payments
│   │   │
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── invoice_serializers.py // Invoice creation, payment serializers
│   │   │   └── wallet_serializers.py // Wallet transaction serializers
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── invoice_views.py    // Invoice management
│   │   │   │                       // Functions: generate_monthly_invoices, pay_invoice, get_invoice_history
│   │   │   ├── wallet_views.py     // Wallet management
│   │   │   │                       // Functions: get_wallet_balance, recharge_wallet, get_transaction_history
│   │   │   ├── payment_views.py    // Payment processing
│   │   │   │                       // Functions: process_payment, handle_payment_callback
│   │   │   └── credit_score_views.py // Credit score system (USP 10)
│   │   │                           // Functions: get_credit_score, update_credit_score, get_score_history
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── invoice_service.py  // Invoice generation and management
│   │   │   ├── wallet_service.py   // Wallet operations
│   │   │   ├── payment_service.py  // Payment gateway integration
│   │   │   └── credit_score_service.py // Credit score calculations
│   │   │
│   │   ├── tasks/                  // Celery background tasks
│   │   │   ├── __init__.py
│   │   │   ├── invoice_tasks.py    // Monthly invoice generation tasks
│   │   │   └── payment_tasks.py    // Payment processing tasks
│   │   │
│   │   ├── urls.py                 // Routes: /invoices/, /wallet/, /payments/, /credit-score/
│   │   ├── permissions.py, validators.py, tests/
│   │
│   ├── operations/                 // App 5: Operations & Safety (USP 11, 12, 13, 14)
│   │   ├── __init__.py
│   │   ├── apps.py, admin.py, migrations/
│   │   │
│   │   ├── models/                 // Database models (3 models)
│   │   │   ├── __init__.py
│   │   │   ├── complaint.py        // Complaint model with AI chatbot integration
│   │   │   ├── entry_log.py        // EntryLog model with night alerts
│   │   │   └── hygiene_rating.py   // HygieneRating model for scorecard
│   │   │
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── complaint_serializers.py // Complaint submission, resolution serializers
│   │   │   ├── entry_serializers.py // Entry/exit logging serializers
│   │   │   └── hygiene_serializers.py // Hygiene rating serializers
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── complaint_views.py  // Complaint management
│   │   │   │                       // Functions: submit_complaint, get_complaints, resolve_complaint
│   │   │   ├── entry_views.py      // Entry/exit logging (USP 12)
│   │   │   │                       // Functions: log_entry_exit, get_entry_history, send_night_alerts
│   │   │   ├── hygiene_views.py    // Hygiene scorecard (USP 13)
│   │   │   │                       // Functions: submit_hygiene_rating, get_hygiene_history
│   │   │   ├── chatbot_views.py    // AI chatbot integration (USP 14)
│   │   │   │                       // Functions: process_whatsapp_message, handle_bot_complaint
│   │   │   └── safety_views.py     // Safety features integration
│   │   │                           // Functions: emergency_protocols, safety_alerts
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── complaint_service.py // Complaint processing business logic
│   │   │   ├── entry_service.py    // Entry logging and alert business logic
│   │   │   ├── hygiene_service.py  // Hygiene tracking business logic
│   │   │   ├── chatbot_service.py  // AI chatbot processing
│   │   │   └── safety_service.py   // Safety and security business logic
│   │   │
│   │   ├── integrations/           // External service integrations
│   │   │   ├── __init__.py
│   │   │   ├── whatsapp_api.py     // WhatsApp Business API integration
│   │   │   ├── sms_gateway.py      // SMS gateway for alerts
│   │   │   └── biometric_api.py    // Biometric device integration
│   │   │
│   │   ├── urls.py                 // Routes: /complaints/, /entry/, /hygiene/, /chatbot/
│   │   ├── permissions.py, validators.py, tests/
│   │
│   └── mess/                       // App 6: Smart Mess Management (USP 15)
│       ├── __init__.py
│       ├── apps.py, admin.py, migrations/
│       │
│       ├── models/                 // Database models (2 models)
│       │   ├── __init__.py
│       │   ├── mess_menu.py        // MessMenu model with daily pricing
│       │   └── daily_meal_selection.py // DailyMealSelection model for pay-per-day
│       │
│       ├── serializers/
│       │   ├── __init__.py
│       │   ├── menu_serializers.py // Menu creation, display serializers
│       │   └── meal_serializers.py // Meal selection, payment serializers
│       │
│       ├── views/
│       │   ├── __init__.py
│       │   ├── menu_views.py       // Menu management
│       │   │                       // Functions: create_daily_menu, get_today_menu, get_weekly_menu
│       │   ├── meal_views.py       // Pay-per-day meal system (USP 15)
│       │   │                       // Functions: book_meal, skip_meal, get_meal_history
│       │   ├── analytics_views.py  // Mess analytics and reporting
│       │   │                       // Functions: get_meal_analytics, get_daily_count, get_waste_report
│       │   └── payment_views.py    // Mess payment integration
│       │                           // Functions: process_meal_payment, refund_skipped_meal
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── menu_service.py     // Menu management business logic
│       │   ├── meal_service.py     // Meal booking and payment business logic
│       │   ├── analytics_service.py // Mess analytics business logic
│       │   └── payment_service.py  // Mess payment processing
│       │
│       ├── tasks/                  // Celery background tasks
│       │   ├── __init__.py
│       │   ├── meal_tasks.py       // Daily meal processing tasks
│       │   └── analytics_tasks.py  // Analytics calculation tasks
│       │
│       ├── urls.py                 // Routes: /menu/, /meals/, /analytics/, /payments/
│       ├── permissions.py, validators.py, tests/
│
├── media/                          // User uploaded files
│   ├── profiles/                   // Profile photos
│   ├── docs/
│   │   └── aadhaar/               // Aadhaar card uploads
│   ├── agreements/                 // Digital agreements
│   ├── complaints/                 // Complaint images
│   └── hygiene/                   // Hygiene photos
│
├── static/                         // Static files (CSS, JS, Images)
│   ├── admin/                      // Django admin static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                      // HTML templates
│   ├── admin/                      // Custom admin templates
│   ├── emails/                     // Email templates
│   └── reports/                    // Report templates
│
├── logs/                           // Application logs
│   ├── django.log                  // Django application logs
│   ├── error.log                   // Error logs
│   ├── celery.log                  // Celery task logs
│   └── audit.log                   // Audit trail logs
│
├── docs/                           // Project documentation
│   ├── api/                        // API documentation
│   ├── deployment/                 // Deployment guides
│   └── development/                // Development setup guides
│
└── tests/                          // Global test files
    ├── __init__.py
    ├── test_settings.py            // Test configuration
    ├── fixtures/                   // Test data fixtures
    └── integration/                // Integration tests
        ├── test_api_integration.py
        └── test_workflow_integration.py
```

---

## COMPLETE FOLDER STRUCTURE SUMMARY

### Total Structure Overview:
- **6 Django Apps**: Modular monolith architecture with clear separation of concerns
- **12 Database Models** distributed across 6 apps
- **15 Unique USPs** implemented across different modules
- **Shared utilities** for common functionality across apps
- **Comprehensive testing** structure for each app
- **Detailed logging** and monitoring setup

### Key File Types Explained:

#### Core Files (Every App Has These):
- **apps.py**: Django app configuration and setup
- **admin.py**: Django admin interface customization
- **models/**: Database models with business logic
- **serializers/**: DRF serializers for API request/response handling
- **views/**: API views and endpoint logic
- **services/**: Business logic layer (core functionality)
- **urls.py**: URL routing for the app
- **permissions.py**: Custom permissions and access control
- **validators.py**: Input validation and data sanitization
- **tests/**: Unit and integration tests

#### App-Specific Structure:

#### 1. Users App (Authentication & User Management):
- **Purpose**: User roles, authentication, parent portal, SOS system
- **Key Features**: JWT authentication, parent-child linking, emergency alerts
- **Models**: CustomUser, TenantProfile (2 models)
- **USPs**: Parent Portal (1), Aadhaar Verification (2), SOS Button (11)

#### 2. Inventory App (Property & Rooms):
- **Purpose**: Room and bed management, pricing, IoT integration
- **Key Features**: Dynamic pricing, public bed links, smart meters
- **Models**: Room, Bed (2 models)
- **USPs**: Public Bed Links (3), Dynamic Pricing (4), Smart Electricity (5)

#### 3. Bookings App (Tenant Lifecycle):
- **Purpose**: Booking management, agreements, AI matching
- **Key Features**: Zero deposit, digital agreements, compatibility matching
- **Models**: Booking (1 model)
- **USPs**: AI Matching (6), Digital Agreement (7), Zero Deposit (8), Auto Refund (9)

#### 4. Finance App (Money Management):
- **Purpose**: Invoicing, payments, wallet, credit scoring
- **Key Features**: Auto invoice generation, wallet system, credit score tracking
- **Models**: Invoice, WalletTransaction (2 models)
- **USPs**: Credit Score System (10)

#### 5. Operations App (Safety & Operations):
- **Purpose**: Complaints, entry logging, hygiene, chatbot
- **Key Features**: WhatsApp bot, biometric entry, hygiene tracking
- **Models**: Complaint, EntryLog, HygieneRating (3 models)
- **USPs**: Night Alerts (12), Hygiene Scorecard (13), AI Chatbot (14)

#### 6. Mess App (Smart Food System):
- **Purpose**: Menu management, pay-per-day meal system
- **Key Features**: Daily meal selection, wallet integration, analytics
- **Models**: MessMenu, DailyMealSelection (2 models)
- **USPs**: Pay-per-Day Mess Wallet (15)

### Inter-App Communication:
- **Direct Python Imports**: Fast synchronous communication between apps
- **Shared Services**: Common business logic in shared/ directory
- **Signal System**: Django signals for event-driven communication
- **Celery Tasks**: Background job processing for heavy operations

### Development & Deployment:
- **Modular Monolith**: All apps in single Django project
- **Single Database**: PostgreSQL with proper model relationships
- **Docker Support**: Containerized deployment with docker-compose
- **Shared Utilities**: Common middleware, validators, and utilities
- **Comprehensive Testing**: Unit and integration tests for each app
- **Centralized Logging**: Django logging with app-specific loggers

### Security Features:
- **JWT Authentication**: Token-based authentication across all apps
- **Role-Based Permissions**: Custom permissions for different user types
- **Input Validation**: Comprehensive request validation in each app
- **Audit Logging**: Complete action tracking for compliance
- **File Upload Security**: Secure handling of user uploads

### Background Tasks (Celery):
- **Invoice Generation**: Monthly automatic invoice creation
- **Payment Processing**: Async payment gateway integration
- **Meal Processing**: Daily meal selection and payment processing
- **Analytics Calculation**: Background analytics and reporting
- **Notification Sending**: Email and SMS notifications

### API Structure:
- **RESTful APIs**: Django REST Framework for all endpoints
- **Consistent Response Format**: Standardized API responses
- **Comprehensive Documentation**: Auto-generated API docs
- **Version Control**: API versioning support
- **Rate Limiting**: API endpoint protection

**✅ COMPLETE DJANGO MODULAR MONOLITH STRUCTURE**: 6 apps with 12 models, 15 USPs implementation, comprehensive file explanations, and beginner-friendly documentation for new developers to understand the complete architecture and file purposes.

---

## Key Development Notes

- **Total Apps**: 6 Django apps in modular monolith architecture
- **Total Models**: 12 models across all apps
- **Communication**: Direct Python imports for fast inter-app communication
- **Database**: Single PostgreSQL database with proper relationships
- **Deployment**: Docker containerization with docker-compose
- **Testing**: Comprehensive test coverage for all apps and features

---

**Document Version**: 1.0
**Last Updated**: 2025-01-27
**Architecture**: Django Modular Monolith
**Total Apps**: 6
**Total Models**: 12
**Total USPs**: 15