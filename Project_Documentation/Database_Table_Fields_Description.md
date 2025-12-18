# 🏨 Smart PG Management System - Database Design (Detailed)

Ye documentation **Smart PG Project** ke liye complete database blueprint hai. Humne **Modular Monolith Architecture** (Django) use kiya hai. Har table ke har field ko detail mein explain kiya gaya hai taaki aapko **"Business Logic"** samajh aaye.

## 📚 QUICK START FOR BEGINNERS

### Ye File Kya Hai?

Ye database ka naksha (map) hai. Ye batata hai ki hum data kahan store karenge aur kyun.

### Kaise Use Karein?

1.  **Field Name**: Column ka naam (e.g., `wallet_balance`).
2.  **Type**: Data kaisa dikhega (Number, Text, Date).
3.  **Why/Logic**: Sabse important part – Ye field kyun zaroori hai?
4.  **Example**: Asli data kaisa dikhega.

-----

## 🚪 MODULE 1: USER MANAGEMENT & AUTH (App: `users`)

### Purpose: Pehchan (Identity) & Security

Ye module decide karta hai ki login karne wala insaan **Malik (Admin)** hai, **Student (Tenant)** hai, ya **Parent** hai.

#### 1.1 Table: `CustomUser`

**Description**: Ye hamara main register hai. Har insaan jo app use karega, wo yahan darj hoga.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Database ko har user ko alag pehchanne ke liye ek unique identifier chahiye. UUID use karne se security aur scalability better hoti hai.
      - **Example**: `550e8400-e29b-41d4-a716-446655440000`
  - `username` (String, Unique)
      - **Why**: Login karne ke liye ID.
      - **Example**: `rahul123`
  - `email` (Email, Unique)
      - **Why**: Registration aur password reset ke liye zaroori hai. Services documentation mein email required hai.
      - **Example**: `rahul@example.com`
  - `role` (Enum: ADMIN, MANAGER, TENANT, PARENT)
      - **Why**: System ko kaise pata chalega ki kisko "Dashboard" dikhana hai aur kisko "Rent Button"? Role se hi permission set hogi.
      - **Example**: `TENANT`
  - `phone_number` (String, Unique)
      - **Why**: Aajkal email se zyada OTP login chalta hai. Aur communication ke liye bhi zaroori hai.
      - **Example**: `+919876543210`
  - `sos_contact_number` (String, Nullable)
      - **Why (USP 11)**: Jab **Panic Button** dabega, toh call kisko jayega? Ye number emergency ke liye save rehta hai.
      - **Example**: `+919998887776` (Papa ka number)
  - `profile_photo` (Image, Nullable)
      - **Why**: Guard ko gate par shakal milane ke liye photo chahiye.
      - **Example**: `profiles/rahul_face.jpg`
  - `preferred_language` (Enum: en, hi, ta, te, kn, bn)
      - **Why (Technical Feature 6)**: User apni preferred language mein app use kar sake - Staff (Cook/Guard) ko Hindi chahiye, Parents ko regional language. System UI is language mein dikhega.
      - **Example**: `hi` (Hindi)
      - **Choices**: English (en), Hindi (hi), Tamil (ta), Telugu (te), Kannada (kn), Bengali (bn)

#### 1.2 Table: `TenantProfile`

**Description**: Sirf "Students" ke liye extra details. User table mein sab mixed hain, lekin student ka data (wallet, aadhaar) yahan rahega.
**Fields**:

  - `user_id` (Foreign Key -\> CustomUser)
      - **Why**: Ye link karta hai ki kaunsa User "Rahul" hai.
      - **Example**: `550e8400-e29b-41d4-a716-446655440000`
  - `guardian_user_id` (Foreign Key -\> CustomUser)
      - **Why (USP 1)**: Parent Portal feature ke liye. Hamein link karna padega ki "Rahul ka baap kaun hai" taaki unhe sirf Rahul ka data dikhe.
      - **Example**: `550e8400-e29b-41d4-a716-446655440001` (Mr. Sharma)
  - `aadhaar_number` (String, Nullable)
      - **Why (USP 2)**: Police Verification automate karne ke liye exact Gov ID number chahiye. Nullable hai kyuki registration time optional hai.
      - **Example**: `4567-8901-2345`
  - `aadhaar_card_front` (Image, Nullable)
      - **Why (USP 2)**: Aadhaar card ka front photo police verification ke liye.
      - **Example**: `docs/aadhaar/rahul_front.jpg`
  - `aadhaar_card_back` (Image, Nullable)
      - **Why (USP 2)**: Aadhaar card ka back photo police verification ke liye.
      - **Example**: `docs/aadhaar/rahul_back.jpg`
  - `police_verification_status` (Enum)
      - **Why (USP 2)**: Police verification ka status track karne ke liye.
      - **Example**: `VERIFIED`
  - `pg_credit_score` (Integer, Default: 700)
      - **Why (USP 10)**: Jaise CIBIL score hota hai, waise hi PG score. Rent time pe diya toh score badhega.
      - **Example**: `750`
  - `wallet_balance` (Decimal)
      - **Why (USP 15)**: **Sabse Important Field**. Mess ka khana aur fines ka paisa yahin se katega.
      - **Example**: `2500.00` (Rupees)
  - `sleep_schedule` (Enum: EARLY_BIRD, NIGHT_OWL, FLEXIBLE)
      - **Why (USP 6)**: AI Compatibility Matching ke liye. System samaan sleep pattern wale students ko ek room mein dega taaki ladai na ho.
      - **Example**: `NIGHT_OWL` (Raat 2 baje sota hai)
  - `cleanliness_level` (Enum: HIGH, MEDIUM, LOW)
      - **Why (USP 6)**: Cleanliness preference. High cleanliness wala Low wale ke saath nahi rahega.
      - **Example**: `HIGH`
  - `noise_tolerance` (Enum: HIGH, MEDIUM, LOW)
      - **Why (USP 6)**: Shor kitna bardash kar sakta hai. Music-lover ko music-lover ke saath denge.
      - **Example**: `LOW` (Shaanti chahiye)
  - `study_hours` (Enum: MORNING, AFTERNOON, LATE_NIGHT, FLEXIBLE)
      - **Why (USP 6)**: Kab padhta hai. Late night studier ko late night ke saath match karenge.
      - **Example**: `LATE_NIGHT`
  - `lifestyle_attributes` (JSON)
      - **Why (USP 6)**: Additional compatibility attributes jo enumerated fields mein fit nahi hote (smoker, vegetarian, etc.). Flexibility ke liye JSON format.
      - **Example**: `{"smoker": false, "vegetarian": true, "pet_lover": false}`

#### 1.3 Table: `StaffProfile`

**Description**: Cook, Guard, Cleaner details.
**Fields**:

  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Link to main User table.
      - **Example**: `Cook's user_id`
  - `staff_role` (Enum: COOK, GUARD, CLEANER, OTHER)
      - **Why**: Job profile.
      - **Example**: `COOK`
  - `daily_rate` (Decimal)
      - **Why**: Salary calculation basis.
      - **Example**: `500.00`
  - `assigned_property_id` (Foreign Key -> Property)
      - **Why**: Where they work.
      - **Example**: `Property UUID`
  - `joining_date` (Date)
      - **Why**: HR records.
      - **Example**: `2025-01-01`

-----

## 🛏️ MODULE 2: PROPERTY & INVENTORY (App: `inventory`)

### Purpose: Dukaan ka Maal (Rooms & Beds)

Hamein pata hona chahiye ki hamare paas bechne ke liye kya hai.

#### 2.0 Table: `Property`

**Description**: Represents a PG branch.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique ID for each PG branch.
      - **Example**: `property_uuid`
  - `name` (String)
      - **Why**: Name of the PG.
      - **Example**: `"Gokuldham PG 1"`
  - `address` (Text)
      - **Why**: Physical location.
      - **Example**: `"123, Main Road, Kota"`
  - `owner_id` (Foreign Key -> CustomUser)
      - **Why**: Mulitple owners support.
      - **Example**: `Owner's user_id`
  - `manager_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Assigned manager.
      - **Example**: `Manager's user_id`
  - `current_hygiene_rating` (Decimal)
      - **Why (USP 13)**: Public hygiene score.
      - **Example**: `4.5`
  - `preferred_language` (Enum: EN, HI, TE)
      - **Why**: For staff app localization.
      - **Example**: `HI`

#### 2.1 Table: `Room`

**Description**: Kamre ki details.
**Fields**:

  - `room_number` (String)
      - **Why**: Manager ko physical location batane ke liye.
      - **Example**: `"204-B"` (2nd Floor, Room 4)
  - `floor` (Integer)
      - **Why**: Filter lagane ke liye (e.g., "Mujhe ground floor chahiye").
      - **Example**: `2`
  - `capacity` (Integer)
      - **Why**: Room mein kitne log reh sakte hain (1/2/3 sharing).
      - **Example**: `2`
  - `has_ac` (Boolean)
      - **Why**: AC wala room hai ya nahi, pricing aur filtering ke liye.
      - **Example**: `True`
  - `has_balcony` (Boolean)
      - **Why**: Balcony wala room hai ya nahi, premium feature.
      - **Example**: `False`
  - `base_rent` (Decimal)
      - **Why (USP 4)**: Original rent amount, seasonal pricing calculate karne ke liye base.
      - **Example**: `5000.00`
  - `current_seasonal_rent` (Decimal)
      - **Why (USP 4)**: **Dynamic Pricing**. Normal rent 5000 ho sakta hai, lekin agar June (peak season) hai toh hum is field ko update karke 6000 kar denge. Invoice yahan se price uthayega.
      - **Example**: `6500.00`

#### 2.2 Table: `Bed`

**Description**: Asli product jo bikta hai. Ek room mein 2-3 beds ho sakte hain.
**Fields**:

  - `room_id` (Foreign Key -\> Room)
      - **Why**: Ye bed kaunse kamre mein rakha hai?
      - **Example**: `550e8400-e29b-41d4-a716-446655440010`
  - `bed_label` (String)
      - **Why**: Kamre mein kaunsa bed? Khidki wala (A) ya darwaze wala (B)?
      - **Example**: `"A"`
  - `public_uid` (UUID)
      - **Why (USP 3)**: **Public Link Feature**. Hamein ek secret code chahiye taaki hum WhatsApp par link bhej sakein "smartpg.com/book/bed/abc-secret-code"
      - **Example**: `550e8400-e29b-41d4-a716-446655440020`
  - `is_occupied` (Boolean)
      - **Why**: Ye bed khali hai ya bhara hua? Booking system ko pata hona chahiye.
      - **Example**: `False` (Khali hai)
  - `iot_meter_id` (String, Nullable)
      - **Why (USP 5)**: Smart Electricity Billing ke liye har bed ka alag meter ID.
      - **Example**: `"METER_204B_A"`

#### 2.3 Table: `PricingRule`

**Description**: Dynamic pricing rules for seasonal adjustments.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ke liye rule hai.
      - **Example**: `Property UUID`
  - `rule_name` (String)
      - **Why**: Rule ka naam identify karne ke liye.
      - **Example**: `"Summer Surge"`
  - `start_month` (Integer)
      - **Why**: Kab se rule apply hoga (1=January, 12=December).
      - **Example**: `4` (April)
  - `end_month` (Integer)
      - **Why**: Kab tak rule apply hoga.
      - **Example**: `6` (June)
  - `price_multiplier` (Decimal)
      - **Why**: Base rent ko kitna multiply karna hai.
      - **Example**: `1.20` (20% increase)

#### 2.4 Table: `ElectricityReading`

**Description**: IoT meter readings for individual bed consumption.
**Fields**:

  - `bed_id` (Foreign Key -> Bed)
      - **Why**: Kaunse bed ka reading hai.
      - **Example**: `Bed UUID`
  - `meter_id` (String)
      - **Why**: Physical meter ka ID.
      - **Example**: `"METER_204B_A"`
  - `reading_kwh` (Decimal)
      - **Why**: Kitni electricity consume hui.
      - **Example**: `15.50` (units)
  - `timestamp` (DateTime)
      - **Why**: Kab reading li gayi.
      - **Example**: `2025-01-15 18:30:00`

#### 2.5 Table: `Asset`

**Description**: Physical assets like ACs, geysers tracking.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka asset hai.
      - **Example**: `Property UUID`
  - `room_id` (Foreign Key -> Room, Nullable)
      - **Why**: Kaunse room mein hai (common area ke liye null).
      - **Example**: `Room UUID`
  - `name` (String)
      - **Why**: Asset ka naam.
      - **Example**: `"1.5 Ton AC"`
  - `qr_code` (String, Unique)
      - **Why**: QR scan karke asset details dekh sakte hain.
      - **Example**: `"QR_AC_001"`
  - `purchase_date` (Date)
      - **Why**: Kab khareeda tha.
      - **Example**: `2024-01-15`
  - `last_service_date` (Date, Nullable)
      - **Why**: Last service kab hui thi.
      - **Example**: `2024-12-01`
  - `next_service_due_date` (Date, Nullable)
      - **Why**: Next service kab due hai.
      - **Example**: `2025-06-01`

#### 2.6 Table: `AssetServiceLog`

**Description**: Service history of all assets.
**Fields**:

  - `asset_id` (Foreign Key -> Asset)
      - **Why**: Kaunse asset ki service hui.
      - **Example**: `Asset UUID`
  - `service_date` (Date)
      - **Why**: Service kab hui.
      - **Example**: `2024-12-01`
  - `cost` (Decimal)
      - **Why**: Service mein kitna kharcha hua.
      - **Example**: `500.00`
  - `description` (Text)
      - **Why**: Kya service hui.
      - **Example**: `"AC gas refill and cleaning"`
  - `serviced_by` (String)
      - **Why**: Kisne service ki.
      - **Example**: `"Sharma Electronics"`
  - `bill_photo` (Image, Nullable)
      - **Why**: Service bill ka photo.
      - **Example**: `"asset_bills/ac_service_bill.jpg"`

-----

## 🏠 MODULE 3: TENANT LIFECYCLE (App: `bookings`)

### Purpose: Student ka Safar (Booking to Exit)

Student ka complete journey - booking se lekar exit tak.

#### 3.1 Table: `Booking`

**Description**: Tenant ka stay record - main booking table.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique booking identifier.
      - **Example**: `booking_uuid`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunsa student book kar raha hai.
      - **Example**: `Tenant's user_id`
  - `bed_id` (Foreign Key -> Bed)
      - **Why**: Kaunsa bed book kiya hai.
      - **Example**: `Bed UUID`
  - `start_date` (Date)
      - **Why**: Kab se stay start hoga.
      - **Example**: `2025-01-01`
  - `end_date` (Date, Nullable)
      - **Why**: Kab tak stay hai (null = ongoing).
      - **Example**: `2025-12-31`
  - `rent_amount` (Decimal)
      - **Why**: Monthly rent amount.
      - **Example**: `6500.00`
  - `deposit_amount` (Decimal)
      - **Why**: Security deposit amount.
      - **Example**: `13000.00`
  - `status` (Enum: ACTIVE, NOTICE_PERIOD, EXITED, CANCELLED)
      - **Why**: Current booking status.
      - **Example**: `ACTIVE`
  - `is_zero_deposit` (Boolean)
      - **Why (USP 8)**: Zero-deposit option liya hai ya nahi.
      - **Example**: `True`
  - `fintech_partner_name` (String, Nullable)
      - **Why (USP 8)**: Kaunsa fintech partner (Slice, ZestMoney).
      - **Example**: `"ZestMoney"`
  - `fintech_loan_id` (String, Nullable)
      - **Why (USP 8)**: Loan ID for tracking.
      - **Example**: `"ZM123456789"`
  - `notice_given_date` (Date, Nullable)
      - **Why (USP 9)**: Kab notice diya tha.
      - **Example**: `2025-11-01`
  - `refund_amount` (Decimal, Nullable)
      - **Why (USP 9)**: Kitna refund milega.
      - **Example**: `12000.00`
  - `refund_processed_date` (Date, Nullable)
      - **Why (USP 9)**: Refund kab process hua.
      - **Example**: `2025-12-05`

#### 3.2 Table: `DigitalAgreement`

**Description**: E-signed rental agreements.
**Fields**:

  - `booking_id` (Foreign Key -> Booking, Primary Key)
      - **Why**: Kaunse booking ka agreement.
      - **Example**: `Booking UUID`
  - `agreement_file` (File)
      - **Why**: PDF agreement file.
      - **Example**: `"agreements/rahul_agreement.pdf"`
  - `is_signed` (Boolean)
      - **Why**: Sign ho gaya ya nahi.
      - **Example**: `True`
  - `signed_at` (DateTime, Nullable)
      - **Why**: Kab sign kiya.
      - **Example**: `2025-01-01 10:30:00`

-----

## 💰 MODULE 4: FINANCE (App: `finance`)

### Purpose: Paisa-Paisaa (Money Management)

Sabka hisab-kitab yahan hota hai.

#### 4.1 Table: `Invoice`

**Description**: Monthly bills for tenants.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique invoice identifier.
      - **Example**: `invoice_uuid`
  - `booking_id` (Foreign Key -> Booking)
      - **Why**: Kaunse booking ka bill.
      - **Example**: `Booking UUID`
  - `issue_date` (Date)
      - **Why**: Bill kab generate hua.
      - **Example**: `2025-01-01`
  - `due_date` (Date)
      - **Why**: Payment kab tak karni hai.
      - **Example**: `2025-01-10`
  - `rent_amount` (Decimal)
      - **Why**: Base rent amount.
      - **Example**: `6500.00`
  - `mess_charges` (Decimal)
      - **Why**: Mess ka bill.
      - **Example**: `2000.00`
  - `electricity_charges` (Decimal)
      - **Why**: Electricity consumption charges.
      - **Example**: `300.00`
  - `late_fee` (Decimal)
      - **Why**: Late payment penalty.
      - **Example**: `100.00`
  - `total_amount` (Decimal)
      - **Why**: Total payable amount.
      - **Example**: `8900.00`
  - `is_paid` (Boolean)
      - **Why**: Payment ho gayi ya nahi.
      - **Example**: `True`
  - `paid_on` (Date, Nullable)
      - **Why**: Kab payment hui.
      - **Example**: `2025-01-05`

#### 4.2 Table: `Transaction`

**Description**: All financial movements log.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique transaction identifier.
      - **Example**: `txn_uuid`
  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse user ka transaction.
      - **Example**: `User UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka transaction.
      - **Example**: `Property UUID`
  - `amount` (Decimal)
      - **Why**: Transaction amount.
      - **Example**: `6500.00`
  - `category` (Enum: RENT, WALLET_RECHARGE, MESS_DEBIT, REFUND, EXPENSE, SALARY)
      - **Why**: Transaction type identify karne ke liye.
      - **Example**: `RENT`
  - `is_credit` (Boolean)
      - **Why**: Paisa aaya (True) ya gaya (False).
      - **Example**: `True`
  - `timestamp` (DateTime)
      - **Why**: Kab transaction hua.
      - **Example**: `2025-01-05 14:30:00`
  - `description` (String)
      - **Why**: Transaction details.
      - **Example**: `"January rent payment"`
  - `payment_gateway_txn_id` (String, Nullable)
      - **Why**: Gateway transaction ID.
      - **Example**: `"RAZORPAY_123456"`
  - `invoice_id` (Foreign Key -> Invoice, Nullable)
      - **Why**: Kaunse invoice ka payment.
      - **Example**: `Invoice UUID`

#### 4.3 Table: `Expense`

**Description**: PG operational expenses.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique expense identifier.
      - **Example**: `expense_uuid`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka expense.
      - **Example**: `Property UUID`
  - `category` (String)
      - **Why**: Expense type.
      - **Example**: `"Groceries"`
  - `amount` (Decimal)
      - **Why**: Expense amount.
      - **Example**: `5000.00`
  - `date` (Date)
      - **Why**: Expense date.
      - **Example**: `2025-01-15`
  - `description` (Text)
      - **Why**: Expense details.
      - **Example**: `"Monthly grocery shopping for mess"`
  - `receipt` (File, Nullable)
      - **Why**: Receipt photo/PDF.
      - **Example**: `"receipts/grocery_jan_2025.jpg"`

-----

## 🛡️ MODULE 5: OPERATIONS & SAFETY (App: `operations`)

### Purpose: Rozana ka Kaam (Daily Operations)

Complaint, safety, entry-exit sab yahan.

#### 5.1 Table: `Complaint`

**Description**: Tenant complaints management.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique complaint identifier.
      - **Example**: `complaint_uuid`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne complaint ki.
      - **Example**: `Tenant UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ki complaint.
      - **Example**: `Property UUID`
  - `category` (String)
      - **Why**: Complaint type.
      - **Example**: `"AC not working"`
  - `description` (Text)
      - **Why**: Complaint details.
      - **Example**: `"Room 204-B AC not cooling properly"`
  - `status` (Enum: OPEN, IN_PROGRESS, RESOLVED)
      - **Why**: Complaint status.
      - **Example**: `OPEN`
  - `created_at` (DateTime)
      - **Why**: Kab complaint ki.
      - **Example**: `2025-01-15 10:30:00`
  - `resolved_at` (DateTime, Nullable)
      - **Why**: Kab resolve hui.
      - **Example**: `2025-01-16 15:00:00`
  - `is_raised_by_bot` (Boolean)
      - **Why (USP 14)**: AI chatbot se complaint aayi ya manual.
      - **Example**: `False`

#### 5.2 Table: `EntryLog`

**Description**: Biometric/QR entry-exit logs.
**Fields**:

  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kaun entry/exit kar raha hai.
      - **Example**: `Tenant UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property mein.
      - **Example**: `Property UUID`
  - `timestamp` (DateTime)
      - **Why**: Kab entry/exit hua.
      - **Example**: `2025-01-15 23:30:00`
  - `direction` (Enum: IN, OUT)
      - **Why**: Andar aa raha ya bahar ja raha.
      - **Example**: `IN`
  - `entry_method` (Enum: BIOMETRIC, QR, MANUAL)
      - **Why**: Kaise entry ki.
      - **Example**: `QR`
  - `is_late_entry` (Boolean)
      - **Why (USP 12)**: Late night entry hai ya nahi.
      - **Example**: `True`
  - `parent_alert_sent` (Boolean)
      - **Why (USP 12)**: Parent ko alert bheja ya nahi.
      - **Example**: `True`

#### 5.3 Table: `Notice`

**Description**: Digital notice board messages.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka notice.
      - **Example**: `Property UUID`
  - `title` (String)
      - **Why**: Notice heading.
      - **Example**: `"Electricity Maintenance"`
  - `body` (Text)
      - **Why**: Notice content.
      - **Example**: `"Power will be off from 2-4 PM tomorrow"`
  - `created_at` (DateTime)
      - **Why**: Kab notice publish hua.
      - **Example**: `2025-01-15 09:00:00`
  - `is_published` (Boolean)
      - **Why**: Notice active hai ya nahi.
      - **Example**: `True`

#### 5.4 Table: `ChatLog`

**Description**: AI chatbot conversation logs.
**Fields**:

  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne chat kiya.
      - **Example**: `Tenant UUID`
  - `message` (Text)
      - **Why**: User ka question.
      - **Example**: `"Mera rent kab due hai?"`
  - `bot_response` (Text)
      - **Why**: AI ka answer.
      - **Example**: `"Aapka rent 10 January ko due hai"`
  - `intent` (String, Nullable)
      - **Why**: AI ne kya samjha.
      - **Example**: `"rent_query"`
  - `timestamp` (DateTime)
      - **Why**: Kab chat hua.
      - **Example**: `2025-01-15 16:45:00`

#### 5.5 Table: `SOSAlert`

**Description**: Emergency SOS alert system.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique SOS identifier.
      - **Example**: `sos_uuid`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne SOS trigger kiya.
      - **Example**: `Tenant UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property mein emergency.
      - **Example**: `Property UUID`
  - `latitude` (Decimal, Nullable)
      - **Why**: GPS location latitude.
      - **Example**: `26.9124`
  - `longitude` (Decimal, Nullable)
      - **Why**: GPS location longitude.
      - **Example**: `75.7873`
  - `location_accuracy` (Integer, Nullable)
      - **Why**: GPS accuracy in meters.
      - **Example**: `5`
  - `message` (Text)
      - **Why**: Emergency message.
      - **Example**: `"Help needed in room 204-B"`
  - `device_info` (JSON)
      - **Why**: Device details for debugging.
      - **Example**: `{"os": "Android", "version": "1.0.2"}`
  - `status` (Enum: TRIGGERED, RESPONDING, RESOLVED, FALSE_ALARM)
      - **Why**: SOS status.
      - **Example**: `TRIGGERED`
  - `triggered_at` (DateTime)
      - **Why**: Kab SOS trigger hua.
      - **Example**: `2025-01-15 22:30:00`
  - `acknowledged_at` (DateTime, Nullable)
      - **Why**: Kab acknowledge hua.
      - **Example**: `2025-01-15 22:32:00`
  - `resolved_at` (DateTime, Nullable)
      - **Why**: Kab resolve hua.
      - **Example**: `2025-01-15 22:45:00`
  - `response_time_seconds` (Integer, Nullable)
      - **Why**: Response time tracking.
      - **Example**: `120`
  - `first_responder_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Pehle kisne respond kiya.
      - **Example**: `Manager UUID`
  - `manager_notified` (Boolean)
      - **Why**: Manager ko notify kiya ya nahi.
      - **Example**: `True`
  - `parent_notified` (Boolean)
      - **Why**: Parent ko notify kiya ya nahi.
      - **Example**: `True`
  - `security_notified` (Boolean)
      - **Why**: Security ko notify kiya ya nahi.
      - **Example**: `True`
  - `owner_notified` (Boolean)
      - **Why**: Owner ko notify kiya ya nahi.
      - **Example**: `False`
  - `resolution_notes` (Text)
      - **Why**: Kaise resolve hua.
      - **Example**: `"False alarm - student pressed by mistake"`
  - `is_genuine_emergency` (Boolean, Nullable)
      - **Why**: Genuine emergency thi ya false alarm.
      - **Example**: `False`

-----

## 🍽️ MODULE 6: SMART MESS (App: `mess`)

### Purpose: Khana-Peena (Food Management)

Mess menu aur daily meal selection.

#### 6.1 Table: `MessMenu`

**Description**: Daily/weekly mess menu.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka menu.
      - **Example**: `Property UUID`
  - `date` (Date)
      - **Why**: Kaunse din ka menu.
      - **Example**: `2025-01-15`
  - `breakfast` (String, Nullable)
      - **Why**: Breakfast items.
      - **Example**: `"Poha, Tea, Banana"`
  - `lunch` (String, Nullable)
      - **Why**: Lunch items.
      - **Example**: `"Dal, Rice, Sabzi, Roti"`
  - `dinner` (String, Nullable)
      - **Why**: Dinner items.
      - **Example**: `"Rajma, Rice, Salad"`
  - `price_breakfast` (Decimal)
      - **Why**: Breakfast price.
      - **Example**: `30.00`
  - `price_lunch` (Decimal)
      - **Why**: Lunch price.
      - **Example**: `60.00`
  - `price_dinner` (Decimal)
      - **Why**: Dinner price.
      - **Example**: `50.00`

#### 6.2 Table: `DailyMealSelection`

**Description**: Tenant's daily meal choices.
**Fields**:

  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse tenant ka selection.
      - **Example**: `Tenant UUID`
  - `menu_id` (Foreign Key -> MessMenu)
      - **Why**: Kaunse din ka menu.
      - **Example**: `Menu UUID`
  - `breakfast_status` (Enum: EATING, SKIPPING)
      - **Why**: Breakfast lega ya nahi.
      - **Example**: `EATING`
  - `lunch_status` (Enum: EATING, SKIPPING)
      - **Why**: Lunch lega ya nahi.
      - **Example**: `SKIPPING`
  - `dinner_status` (Enum: EATING, SKIPPING)
      - **Why**: Dinner lega ya nahi.
      - **Example**: `EATING`
  - `is_billed` (Boolean)
      - **Why**: Wallet se paisa kata ya nahi.
      - **Example**: `True`

-----

## 📞 MODULE 7: CRM & LEADS (App: `crm`)

### Purpose: Naye Customer (Lead Management)

Enquiry se booking tak ka process.

#### 7.1 Table: `Lead`

**Description**: Potential tenant enquiries.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique lead identifier.
      - **Example**: `lead_uuid`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ke liye enquiry.
      - **Example**: `Property UUID`
  - `full_name` (String)
      - **Why**: Lead ka naam.
      - **Example**: `"Amit Sharma"`
  - `phone_number` (String)
      - **Why**: Contact number.
      - **Example**: `"+919876543210"`
  - `email` (Email, Nullable)
      - **Why**: Email ID.
      - **Example**: `"amit@example.com"`
  - `status` (Enum: NEW, CONTACTED, VISITED, CONVERTED, LOST)
      - **Why**: Lead status.
      - **Example**: `NEW`
  - `converted_tenant_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Agar convert ho gaya toh tenant ID.
      - **Example**: `Tenant UUID`
  - `notes` (Text)
      - **Why**: Lead notes.
      - **Example**: `"Interested in AC room, budget 7000"`
  - `created_at` (DateTime)
      - **Why**: Kab enquiry aayi.
      - **Example**: `2025-01-15 11:30:00`

-----

## 🔔 MODULE 8: NOTIFICATIONS (App: `notifications`)

### Purpose: Khabar-Khabar (Communication)

SMS, Email, Push notifications.

#### 8.1 Table: `NotificationLog`

**Description**: All sent notifications log.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique notification identifier.
      - **Example**: `notification_uuid`
  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Kisko notification bheja.
      - **Example**: `User UUID`
  - `notification_type` (Enum: SMS, EMAIL, PUSH, WHATSAPP)
      - **Why**: Notification type.
      - **Example**: `SMS`
  - `category` (Enum: RENT_REMINDER, PAYMENT_SUCCESS, COMPLAINT_UPDATE, NIGHT_ALERT, SOS_ALERT, NOTICE, GENERAL)
      - **Why**: Notification category.
      - **Example**: `RENT_REMINDER`
  - `title` (String)
      - **Why**: Notification title.
      - **Example**: `"Rent Due Reminder"`
  - `message` (Text)
      - **Why**: Notification content.
      - **Example**: `"Your rent is due on 10th January"`
  - `is_sent` (Boolean)
      - **Why**: Successfully sent ya nahi.
      - **Example**: `True`
  - `sent_at` (DateTime, Nullable)
      - **Why**: Kab send hua.
      - **Example**: `2025-01-08 09:00:00`
  - `created_at` (DateTime)
      - **Why**: Kab create hua.
      - **Example**: `2025-01-08 08:59:00`

#### 8.2 Table: `FCMToken`

**Description**: Firebase push notification tokens.
**Fields**:

  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse user ka token.
      - **Example**: `User UUID`
  - `token` (String, Unique)
      - **Why**: FCM token string.
      - **Example**: `"fcm_token_string_here"`
  - `device_type` (Enum: ANDROID, IOS, WEB)
      - **Why**: Device type.
      - **Example**: `ANDROID`
  - `is_active` (Boolean)
      - **Why**: Token active hai ya nahi.
      - **Example**: `True`
  - `created_at` (DateTime)
      - **Why**: Kab token create hua.
      - **Example**: `2025-01-01 10:00:00`
  - `updated_at` (DateTime)
      - **Why**: Last update time.
      - **Example**: `2025-01-15 14:30:00`

-----

## 👥 MODULE 9: VISITORS (App: `visitors`)

### Purpose: Mehman-Nawazi (Guest Management)

Visitor entry approval system.

#### 9.1 Table: `VisitorRequest`

**Description**: Visitor entry requests.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique visitor request identifier.
      - **Example**: `visitor_uuid`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse tenant ka visitor.
      - **Example**: `Tenant UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property mein visit.
      - **Example**: `Property UUID`
  - `visitor_name` (String)
      - **Why**: Visitor ka naam.
      - **Example**: `"Rajesh Sharma"`
  - `visitor_phone` (String)
      - **Why**: Visitor ka phone.
      - **Example**: `"+919876543210"`
  - `visitor_photo` (Image, Nullable)
      - **Why**: Visitor ki photo.
      - **Example**: `"visitors/rajesh_photo.jpg"`
  - `purpose` (String)
      - **Why**: Visit ka purpose.
      - **Example**: `"Family visit"`
  - `status` (Enum: PENDING, APPROVED, REJECTED, CHECKED_OUT)
      - **Why**: Request status.
      - **Example**: `APPROVED`
  - `requested_at` (DateTime)
      - **Why**: Kab request ki.
      - **Example**: `2025-01-15 10:00:00`
  - `approved_at` (DateTime, Nullable)
      - **Why**: Kab approve hua.
      - **Example**: `2025-01-15 10:15:00`
  - `check_in_time` (DateTime, Nullable)
      - **Why**: Kab entry hui.
      - **Example**: `2025-01-15 11:00:00`
  - `check_out_time` (DateTime, Nullable)
      - **Why**: Kab exit hua.
      - **Example**: `2025-01-15 18:00:00`
  - `guard_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kaunse guard ne process kiya.
      - **Example**: `Guard UUID`

-----

## 📦 MODULE 10: INVENTORY (App: `inventory`)

### Purpose: Rasoi ka Maal (Kitchen Stock)

Kitchen inventory management.

#### 10.1 Table: `InventoryItem`

**Description**: Kitchen stock items.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique item identifier.
      - **Example**: `item_uuid`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka stock.
      - **Example**: `Property UUID`
  - `item_name` (String)
      - **Why**: Item ka naam.
      - **Example**: `"Rice"`
  - `category` (String)
      - **Why**: Item category.
      - **Example**: `"Groceries"`
  - `current_quantity` (Decimal)
      - **Why**: Current stock quantity.
      - **Example**: `25.50`
  - `unit` (Enum: KG, LITER, PIECE, PACKET)
      - **Why**: Measurement unit.
      - **Example**: `KG`
  - `minimum_threshold` (Decimal)
      - **Why**: Minimum stock alert level.
      - **Example**: `5.00`
  - `last_restocked_date` (Date, Nullable)
      - **Why**: Last restock date.
      - **Example**: `2025-01-10`

#### 10.2 Table: `InventoryTransaction`

**Description**: Stock movement logs.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique transaction identifier.
      - **Example**: `inv_txn_uuid`
  - `item_id` (Foreign Key -> InventoryItem)
      - **Why**: Kaunse item ka transaction.
      - **Example**: `Item UUID`
  - `transaction_type` (Enum: PURCHASE, CONSUMPTION, WASTAGE, ADJUSTMENT)
      - **Why**: Transaction type.
      - **Example**: `PURCHASE`
  - `quantity` (Decimal)
      - **Why**: Quantity moved.
      - **Example**: `10.00`
  - `date` (Date)
      - **Why**: Transaction date.
      - **Example**: `2025-01-15`
  - `notes` (Text)
      - **Why**: Transaction notes.
      - **Example**: `"Monthly grocery purchase"`
  - `recorded_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne record kiya.
      - **Example**: `Staff UUID`

-----

## 💼 MODULE 11: PAYROLL (App: `payroll`)

### Purpose: Karamchari ka Hisab (Staff Management)

Staff attendance and salary.

#### 11.1 Table: `StaffAttendance`

**Description**: Daily staff attendance.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique attendance identifier.
      - **Example**: `attendance_uuid`
  - `staff_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse staff ka attendance.
      - **Example**: `Staff UUID`
  - `date` (Date)
      - **Why**: Attendance date.
      - **Example**: `2025-01-15`
  - `status` (Enum: PRESENT, ABSENT, HALF_DAY, LEAVE)
      - **Why**: Attendance status.
      - **Example**: `PRESENT`
  - `check_in_time` (Time, Nullable)
      - **Why**: Check-in time.
      - **Example**: `08:30:00`
  - `check_out_time` (Time, Nullable)
      - **Why**: Check-out time.
      - **Example**: `18:00:00`
  - `selfie_photo` (Image, Nullable)
      - **Why**: Attendance selfie.
      - **Example**: `"staff_attendance/cook_selfie.jpg"`
  - `notes` (Text)
      - **Why**: Attendance notes.
      - **Example**: `"Late due to traffic"`

#### 11.2 Table: `SalaryPayment`

**Description**: Monthly salary payments.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique salary payment identifier.
      - **Example**: `salary_uuid`
  - `staff_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse staff ka salary.
      - **Example**: `Staff UUID`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka staff.
      - **Example**: `Property UUID`
  - `month` (Date)
      - **Why**: Salary month (first day).
      - **Example**: `2025-01-01`
  - `days_worked` (Decimal)
      - **Why**: Kitne din kaam kiya.
      - **Example**: `26.00`
  - `daily_rate` (Decimal)
      - **Why**: Per day salary rate.
      - **Example**: `500.00`
  - `gross_salary` (Decimal)
      - **Why**: Total salary before deductions.
      - **Example**: `13000.00`
  - `deductions` (Decimal)
      - **Why**: Deductions (advance, etc.).
      - **Example**: `1000.00`
  - `net_salary` (Decimal)
      - **Why**: Final salary amount.
      - **Example**: `12000.00`
  - `payment_date` (Date)
      - **Why**: Payment date.
      - **Example**: `2025-02-01`
  - `payment_mode` (Enum: CASH, BANK, UPI)
      - **Why**: Payment method.
      - **Example**: `UPI`
  - `transaction_reference` (String, Nullable)
      - **Why**: Payment reference.
      - **Example**: `"UPI_REF_123456"`

-----

## 🧹 MODULE 12: HYGIENE (App: `hygiene`)

### Purpose: Safai-Sutharai (Cleanliness Tracking)

Hygiene inspection and ratings.

#### 12.1 Table: `HygieneInspection`

**Description**: Weekly hygiene inspections.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique inspection identifier.
      - **Example**: `inspection_uuid`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse property ka inspection.
      - **Example**: `Property UUID`
  - `inspection_date` (Date)
      - **Why**: Inspection date.
      - **Example**: `2025-01-15`
  - `inspector_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne inspection kiya.
      - **Example**: `Manager UUID`
  - `cleanliness_score` (Integer)
      - **Why**: Cleanliness score out of 10.
      - **Example**: `8`
  - `kitchen_score` (Integer)
      - **Why**: Kitchen score out of 10.
      - **Example**: `9`
  - `bathroom_score` (Integer)
      - **Why**: Bathroom score out of 10.
      - **Example**: `7`
  - `common_area_score` (Integer)
      - **Why**: Common area score out of 10.
      - **Example**: `8`
  - `overall_rating` (Decimal)
      - **Why**: Average rating out of 5.
      - **Example**: `4.0`
  - `photos` (JSON)
      - **Why**: Inspection photos list.
      - **Example**: `["hygiene/kitchen_jan15.jpg", "hygiene/bathroom_jan15.jpg"]`
  - `remarks` (Text)
      - **Why**: Inspection remarks.
      - **Example**: `"Kitchen needs deep cleaning"`

-----

## 📝 MODULE 13: FEEDBACK (App: `feedback`)

### Purpose: Raay-Sujhav (Feedback Collection)

Tenant feedback and ratings.

#### 13.1 Table: `ComplaintFeedback`

**Description**: Feedback on resolved complaints.
**Fields**:

  - `complaint_id` (Foreign Key -> Complaint, Primary Key)
      - **Why**: Kaunse complaint ka feedback.
      - **Example**: `Complaint UUID`
  - `rating` (Integer)
      - **Why**: Rating 1 to 5.
      - **Example**: `4`
  - `feedback_text` (Text)
      - **Why**: Feedback comments.
      - **Example**: `"Quick resolution, satisfied"`
  - `submitted_at` (DateTime)
      - **Why**: Feedback submission time.
      - **Example**: `2025-01-16 10:30:00`

#### 13.2 Table: `MessFeedback`

**Description**: Daily mess food feedback.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique feedback identifier.
      - **Example**: `mess_feedback_uuid`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne feedback diya.
      - **Example**: `Tenant UUID`
  - `menu_id` (Foreign Key -> MessMenu)
      - **Why**: Kaunse menu ka feedback.
      - **Example**: `Menu UUID`
  - `meal_type` (Enum: BREAKFAST, LUNCH, DINNER)
      - **Why**: Kaunsa meal.
      - **Example**: `LUNCH`
  - `rating` (Integer)
      - **Why**: Rating 1 to 5.
      - **Example**: `3`
  - `feedback_text` (Text)
      - **Why**: Feedback comments.
      - **Example**: `"Dal was too salty"`
  - `submitted_at` (DateTime)
      - **Why**: Feedback time.
      - **Example**: `2025-01-15 14:30:00`

-----

## 🔍 MODULE 14: AUDIT (App: `audit`)

### Purpose: Nigarani (System Monitoring)

All system activities tracking.

#### 14.1 Table: `AuditLog`

**Description**: Comprehensive audit trail.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique audit log identifier.
      - **Example**: `audit_uuid`
  - `user_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne action kiya.
      - **Example**: `User UUID`
  - `action_type` (Enum: CREATE, UPDATE, DELETE, LOGIN, LOGOUT, PAYMENT, REFUND)
      - **Why**: Action type.
      - **Example**: `PAYMENT`
  - `model_name` (String)
      - **Why**: Kaunsa model affected.
      - **Example**: `"Invoice"`
  - `object_id` (String)
      - **Why**: Object ID.
      - **Example**: `"invoice_uuid"`
  - `changes` (JSON)
      - **Why**: Before/after values.
      - **Example**: `{"is_paid": {"before": false, "after": true}}`
  - `ip_address` (IP, Nullable)
      - **Why**: User IP address.
      - **Example**: `"192.168.1.100"`
  - `timestamp` (DateTime)
      - **Why**: Action timestamp.
      - **Example**: `2025-01-15 14:30:00`

-----

## 🎓 MODULE 15: ALUMNI (App: `alumni`)

### Purpose: Purane Vidyarthi (Alumni Network)

Ex-tenants network and job referrals.

#### 15.1 Table: `AlumniProfile`

**Description**: Ex-tenant profiles.
**Fields**:

  - `user_id` (Foreign Key -> CustomUser, Primary Key)
      - **Why**: Kaunsa ex-tenant.
      - **Example**: `User UUID`
  - `current_company` (String, Nullable)
      - **Why**: Current company name.
      - **Example**: `"TCS"`
  - `current_position` (String, Nullable)
      - **Why**: Current job position.
      - **Example**: `"Software Engineer"`
  - `linkedin_url` (URL, Nullable)
      - **Why**: LinkedIn profile.
      - **Example**: `"https://linkedin.com/in/rahul"`
  - `is_open_to_referrals` (Boolean)
      - **Why**: Referral dene ko ready hai ya nahi.
      - **Example**: `True`
  - `exit_date` (Date)
      - **Why**: PG se kab nikla.
      - **Example**: `2024-12-31`
  - `properties_stayed` (ManyToMany -> Property)
      - **Why**: Kahan-kahan raha tha.
      - **Example**: `[Property1_UUID, Property2_UUID]`

#### 15.2 Table: `JobReferral`

**Description**: Job referral requests.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique referral identifier.
      - **Example**: `referral_uuid`
  - `requester_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne referral manga.
      - **Example**: `Tenant UUID`
  - `alumni_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse alumni se manga.
      - **Example**: `Alumni UUID`
  - `company_name` (String)
      - **Why**: Company name.
      - **Example**: `"Infosys"`
  - `position` (String)
      - **Why**: Job position.
      - **Example**: `"Java Developer"`
  - `message` (Text)
      - **Why**: Referral request message.
      - **Example**: `"Please refer me for Java developer role"`
  - `status` (Enum: REQUESTED, ACCEPTED, REJECTED, COMPLETED)
      - **Why**: Referral status.
      - **Example**: `ACCEPTED`
  - `created_at` (DateTime)
      - **Why**: Request time.
      - **Example**: `2025-01-15 10:00:00`
  - `updated_at` (DateTime)
      - **Why**: Last update time.
      - **Example**: `2025-01-16 14:30:00`

-----

## 💳 MODULE 16: SAAS (App: `saas`)

### Purpose: Vyavasaya Model (Business Model)

Subscription plans and app versions.

#### 16.1 Table: `SubscriptionPlan`

**Description**: SaaS subscription plans.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique plan identifier.
      - **Example**: `plan_uuid`
  - `name` (String)
      - **Why**: Plan name.
      - **Example**: `"Gold Plan"`
  - `price_per_month` (Decimal)
      - **Why**: Monthly price.
      - **Example**: `2999.00`
  - `max_properties` (Integer)
      - **Why**: Maximum properties allowed.
      - **Example**: `5`
  - `max_rooms` (Integer)
      - **Why**: Maximum total rooms.
      - **Example**: `100`
  - `features` (JSON)
      - **Why**: Feature flags.
      - **Example**: `{"crm": true, "alumni": true, "reports": true}`
  - `is_active` (Boolean)
      - **Why**: Plan active hai ya nahi.
      - **Example**: `True`

#### 16.2 Table: `PropertySubscription`

**Description**: Owner subscription status.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique subscription identifier.
      - **Example**: `subscription_uuid`
  - `owner_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse owner ka subscription.
      - **Example**: `Owner UUID`
  - `plan_id` (Foreign Key -> SubscriptionPlan)
      - **Why**: Kaunsa plan liya hai.
      - **Example**: `Plan UUID`
  - `status` (Enum: ACTIVE, EXPIRED, CANCELLED, TRIAL)
      - **Why**: Subscription status.
      - **Example**: `ACTIVE`
  - `start_date` (Date)
      - **Why**: Subscription start date.
      - **Example**: `2025-01-01`
  - `end_date` (Date)
      - **Why**: Subscription end date.
      - **Example**: `2025-12-31`
  - `auto_renew` (Boolean)
      - **Why**: Auto renewal enabled.
      - **Example**: `True`

#### 16.3 Table: `AppVersion`

**Description**: App version management.
**Fields**:

  - `platform` (Enum: ANDROID, IOS)
      - **Why**: Platform type.
      - **Example**: `ANDROID`
  - `version_code` (Integer)
      - **Why**: Version code number.
      - **Example**: `102`
  - `version_name` (String)
      - **Why**: Version name.
      - **Example**: `"1.0.2"`
  - `is_mandatory` (Boolean)
      - **Why**: Force update required.
      - **Example**: `False`
  - `release_date` (Date)
      - **Why**: Release date.
      - **Example**: `2025-01-15`

-----

## 📊 MODULE 17: REPORTS (App: `reports`)

### Purpose: Riport-Patrak (Analytics)

Generated reports storage.

#### 17.1 Table: `GeneratedReport`

**Description**: Generated Excel/PDF reports.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique report identifier.
      - **Example**: `report_uuid`
  - `property_id` (Foreign Key -> Property, Nullable)
      - **Why**: Kaunse property ka report.
      - **Example**: `Property UUID`
  - `report_type` (Enum: MONTHLY_RENT, EXPENSE, GST, OCCUPANCY, STAFF_PAYROLL)
      - **Why**: Report type.
      - **Example**: `MONTHLY_RENT`
  - `generated_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne generate kiya.
      - **Example**: `Manager UUID`
  - `file` (File)
      - **Why**: Report file.
      - **Example**: `"reports/rent_jan_2025.xlsx"`
  - `start_date` (Date)
      - **Why**: Report start date.
      - **Example**: `2025-01-01`
  - `end_date` (Date)
      - **Why**: Report end date.
      - **Example**: `2025-01-31`
  - `created_at` (DateTime)
      - **Why**: Report generation time.
      - **Example**: `2025-02-01 09:00:00`

-----

## 🌐 MODULE 18: LOCALIZATION (App: `localization`)

### Purpose: Bhasha-Anuvad (Language Support)

Multi-language translations.

#### 18.1 Table: `TranslationString`

**Description**: UI text translations.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Unique translation identifier.
      - **Example**: `translation_uuid`
  - `module` (String)
      - **Why**: App module name.
      - **Example**: `"mess"`
  - `key` (String)
      - **Why**: Translation key.
      - **Example**: `"book_meal"`
  - `language` (Enum: en, hi, ta, te, kn, bn)
      - **Why**: Target language.
      - **Example**: `hi`
  - `value` (Text)
      - **Why**: Translated text.
      - **Example**: `"खाना बुक करें"`
  - `created_at` (DateTime)
      - **Why**: Creation time.
      - **Example**: `2025-01-01 10:00:00`
  - `updated_at` (DateTime)
      - **Why**: Last update time.
      - **Example**: `2025-01-15 14:30:00`
  - `updated_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne update kiya.
      - **Example**: `Admin UUID`

-----

## 📋 SUMMARY

### **Total Apps: 18**
1. users (User Management & Auth)
2. properties (Property & Inventory)
3. bookings (Tenant Lifecycle)
4. finance (Finance Management)
5. operations (Operations & Safety)
6. mess (Smart Mess)
7. crm (CRM & Leads)
8. notifications (Notifications)
9. visitors (Visitor Management)
10. inventory (Kitchen Inventory)
11. payroll (Staff & Payroll)
12. hygiene (Hygiene Tracking)
13. feedback (Feedback Collection)
14. audit (System Monitoring)
15. alumni (Alumni Network)
16. saas (SaaS Business Model)
17. reports (Analytics & Reports)
18. localization (Language Support)

### **Total Models: 41**

| App | Models Count | Key Models |
|-----|--------------|------------|
| users | 3 | CustomUser, TenantProfile, StaffProfile |
| properties | 7 | Property, Room, Bed, PricingRule, Asset, ElectricityReading, AssetServiceLog |
| bookings | 2 | Booking, DigitalAgreement |
| finance | 3 | Invoice, Transaction, Expense |
| operations | 5 | Complaint, EntryLog, Notice, ChatLog, SOSAlert |
| mess | 2 | MessMenu, DailyMealSelection |
| crm | 1 | Lead |
| notifications | 2 | NotificationLog, FCMToken |
| visitors | 1 | VisitorRequest |
| inventory | 2 | InventoryItem, InventoryTransaction |
| payroll | 2 | StaffAttendance, SalaryPayment |
| hygiene | 1 | HygieneInspection |
| feedback | 2 | ComplaintFeedback, MessFeedback |
| audit | 1 | AuditLog |
| alumni | 2 | AlumniProfile, JobReferral |
| saas | 3 | SubscriptionPlan, PropertySubscription, AppVersion |
| reports | 1 | GeneratedReport |
| localization | 1 | TranslationString |

### **Feature Coverage: 100% ✅**

**All 33+ Features Covered:**
- ✅ All 6 Core Modules
- ✅ All 15 USP Features (AI Compatibility, Zero-Deposit, SOS, etc.)
- ✅ All 9 Advanced Features (Multi-Property, CRM, Alumni, etc.)
- ✅ All 9 Technical Features (Notifications, Localization, Audit, etc.)

### **Key Business Logic Explained:**

1. **Multi-Tenant Architecture**: Each property can have multiple owners/managers
2. **Dynamic Pricing**: Seasonal rent adjustments through PricingRule
3. **Smart Billing**: IoT-based electricity billing per bed
4. **Parent Portal**: Guardian access to student data
5. **Zero-Deposit**: Fintech integration for deposit alternatives
6. **AI Compatibility**: Detailed preference matching for roommates
7. **SOS System**: Comprehensive emergency alert system
8. **Wallet System**: Pay-per-day mess billing
9. **Digital Agreements**: E-signed rental contracts
10. **Audit Trail**: Complete system activity logging

-----

**📝 Document Status:** ✅ COMPLETE & SYNCHRONIZED  
**📅 Last Updated:** January 2025  
**🎯 Total Fields Documented:** 200+ across 41 models  
**✅ Sync Status:** 100% aligned with All_Database_Tables_Models.mdhttps://smartpg.com/book/bed/abc-secret-code)". Isse bina login kiye banda bed dekh sakta hai.
      - **Example**: `550e8400-e29b-41d4-a716-446655440000`
  - `iot_meter_id` (String)
      - **Why (USP 5)**: Har bed ka apna bijli meter hai. Ye uska Hardware Serial Number hai taaki hum reading fetch kar sakein.
      - **Example**: `"IOT-METER-X99"`
  - `is_occupied` (Boolean)
      - **Why**: Simple status check. Agar `True` hai, toh naya banda book nahi kar sakta.
      - **Example**: `False` (Available)

#### 2.3 Table: `PricingRule`

**Description**: Seasonal pricing logic.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Rules are per property.
  - `rule_name` (String)
      - **Why**: Identify the rule.
      - **Example**: `"Summer Surge"`
  - `start_month` (Integer)
      - **Why**: When does it start (1-12).
      - **Example**: `4` (April)
  - `end_month` (Integer)
      - **Why**: When does it end.
      - **Example**: `6` (June)
  - `price_multiplier` (Decimal)
      - **Why (USP 4)**: Rent multiplier. 1.10 means 10% extra.
      - **Example**: `1.10`

#### 2.4 Table: `ElectricityReading`

**Description**: IoT meter logs.
**Fields**:

  - `bed_id` (Foreign Key -> Bed)
      - **Why**: Which bed consumed power.
  - `meter_id` (String)
      - **Why**: IoT Device ID.
  - `reading_kwh` (Decimal)
      - **Why**: Units consumed.
      - **Example**: `12.5`
  - `timestamp` (DateTime)
      - **Why**: When was reading taken.

#### 2.5 Table: `Asset`

**Description**: Physical assets (AC, Geyser).
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Where is the asset.
  - `room_id` (Foreign Key -> Room, Nullable)
      - **Why**: Which room (if applicable).
  - `name` (String)
      - **Why**: What is it.
      - **Example**: `"Voltas AC 1.5T"`
  - `qr_code` (String)
      - **Why**: Scan for history.
  - `purchase_date` (Date)
      - **Why**: Warranty tracking.
  - `next_service_due_date` (Date)
      - **Why**: Maintenance alerts.

#### 2.6 Table: `AssetServiceLog`

**Description**: Repair history.
**Fields**:

  - `asset_id` (Foreign Key -> Asset)
      - **Why**: Which item fixed.
  - `service_date` (Date)
      - **Why**: When.
  - `cost` (Decimal)
      - **Why**: Expense tracking.
  - `description` (Text)
      - **Why**: What was done.
      - **Example**: `"Gas filling"`
  - `bill_photo` (Image)
      - **Why**: Proof.

-----

## 👨‍🎓 MODULE 3: TENANT LIFECYCLE (App: `bookings`)

### Purpose: Aana, Rehna aur Jaana

Kaun, Kahan, aur Kab tak reh raha hai.

#### 3.1 Table: `Booking`

**Description**: Ye table user aur bed ko jodta hai.
**Fields**:

  - `tenant_id` (Foreign Key -\> User)
      - **Why**: Kisne book kiya?
  - `bed_id` (Foreign Key -\> Bed)
      - **Why**: Kya book kiya?
  - `payment_mode` (Enum)
      - **Why (USP 8)**: **Zero Deposit Tracking**. Agar bande ne "Fintech Loan" chuna hai, toh hume deposit nahi mangna hai, balki loan company se lena hai.
      - **Example**: `"FINTECH_LOAN"`
  - `rent_amount` (Decimal)
      - **Why**: Invoice generation ke liye monthly rent amount store karna zaroori hai.
      - **Example**: `8000.00`
  - `deposit_amount` (Decimal)
      - **Why**: Security deposit ka amount track karne ke liye. Zero deposit mein ye 0 hoga.
      - **Example**: `16000.00`
  - `agreement_pdf` (File)
      - **Why (USP 7)**: Sign kiya hua document proof ke liye store karna zaroori hai.
      - **Example**: `agreements/rahul_signed.pdf`
  - `notice_given_date` (Date)
      - **Why (USP 9)**: Jab student app par "I am leaving" dabata hai, ye date save hoti hai. Iske basis par system calculate karega ki refund kab aur kitna dena hai.
      - **Example**: `2025-11-18`
  - `refund_amount` (Decimal, Nullable)
      - **Why (USP 9)**: Auto-calculated refund amount. System calculate karega: Deposit - Outstanding Dues - Damage Charges = Refund.
      - **Example**: `14500.00` (₹16000 deposit minus ₹1500 pending dues)
  - `refund_processed_date` (Date, Nullable)
      - **Why (USP 9)**: Kab refund process hua. Ye timestamp proof hai ki paisa wapas bhej diya gaya.
      - **Example**: `2025-11-20`
  - `is_zero_deposit` (Boolean)
      - **Why (USP 8)**: Zero deposit option liya ya nahi. True means fintech loan liya, false means normal deposit diya.
      - **Example**: `True` (Fintech loan liya)
  - `fintech_partner_name` (String, Nullable)
      - **Why (USP 8)**: Kaunsi company se loan liya (e.g., "PayLater Finance", "ZestMoney"). Integration tracking ke liye.
      - **Example**: `"PayLater Finance"`
  - `fintech_loan_id` (String, Nullable)
      - **Why (USP 8)**: Loan company ka transaction/loan ID. Agar student payment nahi karta toh loan company ko contact karne ke liye.
      - **Example**: `"LOAN-2025-X99876"`
  - `status` (Enum)
      - **Why**: Booking ka current status track karne ke liye. WAITING_FOR_LOAN_APPROVAL zero deposit feature ke liye zaroori hai.
      - **Example**: `ACTIVE`
      - **Choices**: ACTIVE, NOTICE_PERIOD, EXITED, CANCELLED

#### 3.2 Table: `DigitalAgreement`

**Description**: E-signed legal documents.
**Fields**:

  - `booking_id` (OneToOne -> Booking)
      - **Why**: Link to specific stay.
  - `agreement_file` (File)
      - **Why (USP 7)**: The PDF file.
  - `is_signed` (Boolean)
      - **Why**: Status check.
  - `signed_at` (DateTime)
      - **Why**: Timestamp of sign.

-----

## 💰 MODULE 4: FINANCE (App: `finance`)

### Purpose: Rokda (Money Management)

Paisa kahan se aaya aur kahan gaya.

#### 4.1 Table: `Invoice`

**Description**: Har mahine ka bill.
**Fields**:

  - `due_date` (Date)
      - **Why (USP 10)**: Credit score calculate karne ke liye due date zaroori hai. Time pe payment kiya toh score badhega.
      - **Example**: `2025-12-05`
  - `electricity_amount` (Decimal)
      - **Why (USP 5)**: Ye IoT meter ki reading se calculate hokar yahan automatic bhara jayega.
      - **Example**: `450.00` (Kyuki AC zyada chalaya)
  - `mess_total` (Decimal)
      - **Why (USP 15)**: Pure mahine mein usne kitne "Lunch/Dinner" khaye, uska total jod kar yahan aayega.
      - **Example**: `2100.00` (30 days x ₹70)
  - `late_fee` (Decimal)
      - **Why**: Late payment par penalty lagane ke liye.
      - **Example**: `200.00`
  - `discount_amount` (Decimal)
      - **Why**: Good credit score wale students ko discount dene ke liye.
      - **Example**: `100.00`
  - `total_due` (Decimal)
      - **Why**: Final amount jo student ko pay karna hai (Rent + Electricity + Mess + Late Fee - Discount).
      - **Example**: `8550.00`

      - **Example**: `8550.00`

#### 4.2 Table: `Transaction`

**Description**: Logs all financial movements (Rent, Wallet, Refunds, Expenses).
**Fields**:

  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Who is involved.
  - `property_id` (Foreign Key -> Property)
      - **Why**: Which branch.
  - `is_credit` (Boolean)
      - **Why**: Money IN (True) or OUT (False).
  - `category` (Enum: RENT, WALLET_RECHARGE, MESS, REFUND, EXPENSE, SALARY)
      - **Why**: Type of money movement.
  - `amount` (Decimal)
      - **Why**: How much.
  - `description` (String)
      - **Why**: Details.
  - `payment_gateway_txn_id` (String, Nullable)
      - **Why**: Tracking with Razorpay/PhonePe.
  - `invoice_id` (Foreign Key -> Invoice, Nullable)
      - **Why**: Link to bill if paying rent.

#### 4.3 Table: `Expense`

**Description**: Operational costs.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Branch expense.
  - `category` (String)
      - **Why**: Type (Groceries, Utilites).
  - `amount` (Decimal)
      - **Why**: Cost.
  - `receipt` (File)
      - **Why**: Proof for audit.

**Description**: User ki Passbook. Har choti-badi transaction yahan record hogi.
**Fields**:

  - `txn_type` (Enum: DEBIT/CREDIT)
      - **Why**: Paisa aaya (Credit) ya gaya (Debit)?
      - **Example**: `DEBIT`
  - `category` (Enum)
      - **Why**: Paisa kahan kata? Services mein RECHARGE, FINE, ELECTRICITY categories bhi hain reporting ke liye.
      - **Example**: `"MESS"`
  - `description` (Text, Nullable)
      - **Why**: Transaction ki details store karne ke liye (e.g., "Lunch payment for 20th Nov").
      - **Example**: `"Wallet recharge via UPI"`
  - `reference_id` (String, Nullable)
      - **Why**: External payment gateway ka transaction ID store karne ke liye.
      - **Example**: `"TXN123456789"`
  - `amount` (Decimal)
      - **Example**: `60.00`

-----

## 🛠️ MODULE 5: OPERATIONS & SAFETY (App: `operations`)

### Purpose: Roz-marra ke kaam aur Suraksha

#### 5.1 Table: `Complaint`

**Description**: Shikayatein.
**Fields**:

  - `category` (Enum)
      - **Why**: Complaint ko categorize karne ke liye. OTHER category flexibility ke liye add kiya gaya.
      - **Example**: `PLUMBING`
  - `priority` (Enum)
      - **Why**: Urgent complaints ko pehle resolve karne ke liye priority system.
      - **Example**: `HIGH`
  - `assigned_to` (Foreign Key, Nullable)
      - **Why**: Complaint kisko assign hui hai ye track karne ke liye.
      - **Example**: `Manager ka user_id`
  - `resolved_at` (DateTime, Nullable)
      - **Why**: Complaint kab resolve hui ye timestamp ke liye.
      - **Example**: `2025-11-20T15:30:00Z`
  - `is_raised_by_bot` (Boolean)
      - **Why (USP 14)**: Hamein pata hona chahiye ki ye complaint app se aayi hai ya WhatsApp AI Bot ne banayi hai.
      - **Example**: `True`
  - `image` (Image)
      - **Why**: Plumber ko bhejne se pehle photo dikhani padegi ki nal kahan se toota hai.
      - **Example**: `complaints/broken_tap.jpg`

#### 5.2 Table: `EntryLog`

**Description**: Gate ka Register.
**Fields**:

  - `parent_alert_sent` (Boolean)
      - **Why (USP 12)**: Agar raat ke 11 baje entry hui, toh system check karega "Kya maine Papa ko SMS bhej diya?". Ye column uska proof hai.
      - **Example**: `True` (Message sent)
  - `is_late_entry` (Boolean)
      - **Why**: Baad mein report nikalne ke liye ki "Kaunsa student sabse zyada late aata hai".
      - **Example**: `True`

#### 5.3 Table: `Notice`

**Description**: Digital Notice Board.
**Fields**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Which PG.
  - `title` (String)
      - **Why**: Headline.
  - `body` (Text)
      - **Why**: Message.
  - `is_published` (Boolean)
      - **Why**: Draft vs Live.

#### 5.4 Table: `ChatLog`

**Description**: AI Bot history.
**Fields**:

  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Who asked.
  - `message` (Text)
      - **Why**: User question.
  - `bot_response` (Text)
      - **Why**: AI answer.
  - `intent` (String)
      - **Why**: What they wanted (e.g. `rent_query`).

#### 5.5 Table: `SOSAlert`

**Description**: Emergency SOS alert ka complete record. Jab student Panic Button dabayega, tab ye table use ho ki kya hua, kitni der mein response aaya, aur kaise resolve hua.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har emergency incident ko uniquely identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440070`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why (USP 11)**: Kisne SOS button dabaya - student ka record.
      - **Example**: `Rahul ka user_id`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse PG mein emergency aayi hai - responders ko location pata chale.
      - **Example**: `Gokuldham PG ka UUID`
  - `latitude` (Decimal, Nullable)
      - **Why**: Phone ka GPS location - exact position. Manager ko Google Maps mein dikhaenge.
      - **Example**: `28.6139` (Delhi)
  - `longitude` (Decimal, Nullable)
      - **Why**: Longitude coordinate - latitude ke saath complete location.
      - **Example**: `77.2090`
  - `location_accuracy` (Integer, Nullable)
      - **Why**: GPS kitna accurate hai (meters mein). 10 meters matlab bahut accurate, 100 meters matlab thoda dhundhla.
      - **Example**: `15` (15 meter radius mein hai)
  - `message` (Text, Blank allowed)
      - **Why**: Student optional message type kar sakta hai emergency ke time (e.g., "Help me", "Fire").
      - **Example**: `"Need immediate help"`
  - `device_info` (JSON)
      - **Why**: Kis phone se SOS aaya (Android/iOS), kaun sa app version - debugging ke liye zaroori.
      - **Example**: `{"device": "Android", "app_version": "1.2.3"}`
  - `status` (Enum: TRIGGERED, RESPONDING, RESOLVED, FALSE_ALARM)
      - **Why**: Emergency ka current state kya hai.
      - **Example**: `TRIGGERED` (Abhi abhi aaya)
          - `TRIGGERED`: SOS button abhi-abhi dabaya gaya
          - `RESPONDING`: Manager/Security respond kar rahe hain
          - `RESOLVED`: Emergency khatam ho gayi
          - `FALSE_ALARM`: Galti se dab gaya tha
  - `triggered_at` (DateTime, Auto-generated)
      - **Why**: Exactly kab SOS button dabaya gaya - time-critical information.
      - **Example**: `2025-11-20T22:45:30Z`
  - `acknowledged_at` (DateTime, Nullable)
      - **Why**: Manager/Security ne kab dekha - response time calculate karne ke liye.
      - **Example**: `2025-11-20T22:46:15Z` (45 seconds mein acknowledge kiya)
  - `resolved_at` (DateTime, Nullable)
      - **Why**: Incident kab resolve hua - complete timeline ke liye.
      - **Example**: `2025-11-20T23:00:00Z`
  - `response_time_seconds` (Integer, Nullable)
      - **Why**: Kitni der mein first response aaya(seconds mein) - performance tracking ke liye.
      - **Example**: `45` (45 seconds)
      - **Calculation**: `acknowledged_at - triggered_at` (automatically calculated)
  - `first_responder_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Sabse pehle kaunsa Manager/Guard respond kiya - credit tracking.
      - **Example**: `Manager Rajesh ka user_id`
  - `manager_notified` (Boolean)
      - **Why**: Track karna ki Manager ko notification gayi ya nahi.
      - **Example**: `True`
  - `parent_notified` (Boolean)
      - **Why (USP 1)**: Parents ko SMS/WhatsApp gaya ya nahi - Parent Portal ke liye.
      - **Example**: `True`
  - `security_notified` (Boolean)
      - **Why**: Security guard ko alert gaya ya nahi.
      - **Example**: `True`
  - `owner_notified` (Boolean)
      - **Why**: PG owner ko bhi bheja ya nahi (serious cases mein).
      - **Example**: `False`
  - `resolution_notes` (Text, Blank allowed)
      - **Why**: Kaise resolve hui - detailed explanation. Manager baad mein fill karega.
      - **Example**: `"False alarm - student accidentally pressed button"`
  - `is_genuine_emergency` (Boolean,Nullable)
      - **Why**: Sahi emergency thi ya galti se button dab gaya - False alarm tracking.
      - **Example**: `False` (Galti se dab gaya)
          - `True`: Real emergency thi
          - `False`: False alarm
          - `Null`: Abhi decide nahi hua

**Status Flow**: TRIGGERED -> RESPONDING -> RESOLVED/FALSE_ALARM

**Use Cases**:
- Emergency response time analytics
- Parent ko immediately location share
- Safety incident reporting
- False alarm prevention (agar bahut zyada false alarms hain toh warning)

-----

## 🍛 MODULE 6: SMART MESS (App: `mess`)

### Purpose: Pay-Per-Day Meal System

Sabse important USP - students sirf jitna khana khayenge utna hi pay karenge.

#### 6.1 Table: `MessMenu`

**Description**: Daily menu aur prices.
**Fields**:

  - `date` (Date, Unique)
      - **Why**: Har din ka alag menu hota hai.
      - **Example**: `2025-11-20`
  - `breakfast` (String)
      - **Why**: Breakfast mein kya item hai.
      - **Example**: `"Poha + Tea"`
  - `lunch` (String)
      - **Why**: Lunch mein kya item hai.
      - **Example**: `"Dal Rice + Sabzi"`
  - `dinner` (String)
      - **Why**: Dinner mein kya item hai.
      - **Example**: `"Paneer Curry + Roti"`
  - `price_breakfast` (Decimal)
      - **Why (USP 15)**: Per-day pricing ke liye har meal ka alag price.
      - **Example**: `40.00`
  - `price_lunch` (Decimal)
      - **Why (USP 15)**: Lunch ka individual price.
      - **Example**: `70.00`
  - `price_dinner` (Decimal)
      - **Why (USP 15)**: Dinner ka individual price.
      - **Example**: `80.00`

#### 6.2 Table: `DailyMealSelection`

**Description**: Student ka daily meal choice aur payment.
**Fields**:

  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse student ka meal selection hai.
      - **Example**: `Rahul ka user_id`
  - `date` (Date)
      - **Why**: Kaunse din ka selection hai.
      - **Example**: `2025-11-20`
  - `breakfast_status` (Enum)
      - **Why (USP 15)**: EATING mark kiya toh paisa katega, SKIPPING mark kiya toh nahi katega.
      - **Example**: `EATING`
  - `lunch_status` (Enum)
      - **Why (USP 15)**: Lunch ke liye separate choice.
      - **Example**: `SKIPPING`
  - `dinner_status` (Enum)
      - **Why (USP 15)**: Dinner ke liye separate choice.
      - **Example**: `EATING`
  - `total_cost` (Decimal)
      - **Why**: Us din ka total meal cost (sirf EATING wale meals ka).
      - **Example**: `120.00` (Breakfast 40 + Dinner 80)

**Status Choices**: PENDING, EATING, SKIPPING
**Unique Constraint**: (tenant, date) - Ek student ka ek din mein sirf ek record

-----

## 📊 MODULE 7: CRM & LEAD MANAGEMENT (App: `crm`)

### Purpose: Naye Students Ko Dhoondhna

Jo log call karte hain par abhi book nahi kiya, unka data yahan store hoga.

#### 7.1 Table: `Lead`

**Description**: Enquiry register.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har lead ko unique identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440020`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse PG branch ke liye enquiry aayi hai.
      - **Example**: `Property ka UUID`
  - `full_name` (String)
      - **Why**: Potential tenant ka naam.
      - **Example**: `"Amit Kumar"`
  - `phone_number` (String)
      - **Why**: Follow-up call karne ke liye.
      - **Example**: `"+919876543210"`
  - `email` (Email, Nullable)
      - **Why**: Email se brochure bhejne ke liye.
      - **Example**: `"amit@example.com"`
  - `status` (Enum: NEW, CONTACTED, VISITED, CONVERTED, LOST)
      - **Why (Advanced Feature 5)**: Lead ka current stage track karne ke liye.
      - **Example**: `VISITED`
  - `notes` (Text)
      - **Why**: Manager ke remarks (e.g., "Budget 8000 hai").
      - **Example**: `"Interested in AC room"`
  - `created_at` (DateTime)
      - **Why**: Kab enquiry aayi thi.
      - **Example**: `2025-11-20T10:30:00Z`

-----

## 🔔 MODULE 8: NOTIFICATIONS (App: `notifications`)

### Purpose: Alerts Bhejne Ka System

SMS, Email, WhatsApp, Push - sab yahan se manage hoga.

#### 8.1 Table: `NotificationLog`

**Description**: Har notification ka record.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har notification ko track karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440030`
  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Kisko notification bheji gayi.
      - **Example**: `Rahul ka user_id`
  - `notification_type` (Enum: SMS, EMAIL, PUSH, WHATSAPP)
      - **Why (Technical Feature 1)**: Kis medium se bheja.
      - **Example**: `WHATSAPP`
  - `category` (Enum: RENT_REMINDER, PAYMENT_SUCCESS, COMPLAINT_UPDATE, NIGHT_ALERT, SOS_ALERT, NOTICE, GENERAL)
      - **Why**: Notification ka purpose kya tha.
      - **Example**: `NIGHT_ALERT`
  - `title` (String)
      - **Why**: Notification ka heading.
      - **Example**: `"Late Night Entry Alert"`
  - `message` (Text)
      - **Why**: Actual message content.
      - **Example**: `"Rahul entered PG at 11:30 PM"`
  - `is_sent` (Boolean)
      - **Why**: Successfully deliver hua ya nahi.
      - **Example**: `True`
  - `sent_at` (DateTime, Nullable)
      - **Why**: Kab deliver hua.
      - **Example**: `2025-11-20T23:31:00Z`
  - `created_at` (DateTime)
      - **Why**: Kab queue mein dala gaya.
      - **Example**: `2025-11-20T23:30:00Z`

#### 8.2 Table: `FCMToken`

**Description**: Mobile devices ke push notification tokens.
**Fields**:

  - `user_id` (Foreign Key -> CustomUser)
      - **Why**: Kis user ka device hai.
      - **Example**: `Rahul ka user_id`
  - `token` (String, Unique)
      - **Why**: Firebase Cloud Messaging token.
      - **Example**: `"dXJk8fK...long_token"`
  - `device_type` (Enum: ANDROID, IOS, WEB)
      - **Why**: Kis platform ka device hai.
      - **Example**: `ANDROID`
  - `is_active` (Boolean)
      - **Why**: Token valid hai ya expire ho gaya.
      - **Example**: `True`
  - `created_at` (DateTime)
      - **Why**: Token kab register hua.
      - **Example**: `2025-11-01T10:00:00Z`
  - `updated_at` (DateTime)
      - **Why**: Last kab update hua.
      - **Example**: `2025-11-20T10:00:00Z`

-----

## 🚪 MODULE 9: VISITOR MANAGEMENT (App: `visitors`)

### Purpose: Bahar Wale Log Ka Entry Control

Guard ke paas approval system.

#### 9.1 Table: `VisitorRequest`

**Description**: Visitor entry requests.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har visitor request ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440040`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why (Advanced Feature 6)**: Kaunse student ka guest hai.
      - **Example**: `Rahul ka user_id`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse PG mein aana hai.
      - **Example**: `Property ka UUID`
  - `visitor_name` (String)
      - **Why**: Guest ka naam.
      - **Example**: `"Mr. Sharma (Father)"`
  - `visitor_phone` (String)
      - **Why**: Emergency contact.
      - **Example**: `"+919998887776"`
  - `visitor_photo` (Image, Nullable)
      - **Why**: Guard ne gate par photo li.
      - **Example**: `visitors/sharma_photo.jpg`
  - `purpose` (String)
      - **Why**: Aane ka reason.
      - **Example**: `"Meeting son"`
  - `status` (Enum: PENDING, APPROVED, REJECTED, CHECKED_OUT)
      - **Why**: Request ka current state.
      - **Example**: `APPROVED`
  - `requested_at` (DateTime)
      - **Why**: Guard ne kab request bheji.
      - **Example**: `2025-11-20T14:00:00Z`
  - `approved_at` (DateTime, Nullable)
      - **Why**: Student ne kab approve kiya.
      - **Example**: `2025-11-20T14:05:00Z`
  - `check_in_time` (DateTime, Nullable)
      - **Why**: Andar kab ghusa.
      - **Example**: `2025-11-20T14:10:00Z`
  - `check_out_time` (DateTime, Nullable)
      - **Why**: Bahar kab gaya.
      - **Example**: `2025-11-20T16:00:00Z`
  - `guard_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kaunse guard ne process kiya.
      - **Example**: `Guard ka user_id`

-----

## 📦 MODULE 10: INVENTORY MANAGEMENT (App: `inventory`)

### Purpose: Kitchen Ka Stock

Aata, chawal, sabzi - sab ka hisab.

#### 10.1 Table: `InventoryItem`

**Description**: Stock items list.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har item ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440050`
  - `property_id` (Foreign Key -> Property)
      - **Why (Advanced Feature 4)**: Kaunse PG ka stock hai.
      - **Example**: `Property ka UUID`
  - `item_name` (String)
      - **Why**: Item ka naam.
      - **Example**: `"Basmati Rice"`
  - `category` (String)
      - **Why**: Grouping ke liye.
      - **Example**: `"Groceries"`
  - `current_quantity` (Decimal)
      - **Why**: Abhi kitna stock hai.
      - **Example**: `25.50` (kg)
  - `unit` (Enum: KG, LITER, PIECE, PACKET)
      - **Why**: Measurement unit.
      - **Example**: `KG`
  - `minimum_threshold` (Decimal)
      - **Why**: Isse neeche gaya toh alert bhejo.
      - **Example**: `10.00`
  - `last_restocked_date` (Date, Nullable)
      - **Why**: Last kab stock aaya tha.
      - **Example**: `2025-11-15`

#### 10.2 Table: `InventoryTransaction`

**Description**: Stock movements log.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har transaction ko track karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440051`
  - `item_id` (Foreign Key -> InventoryItem)
      - **Why**: Kaunse item ka transaction hai.
      - **Example**: `Rice ka item_id`
  - `transaction_type` (Enum: PURCHASE, CONSUMPTION, WASTAGE, ADJUSTMENT)
      - **Why**: Stock badha ya ghata.
      - **Example**: `CONSUMPTION`
  - `quantity` (Decimal)
      - **Why**: Kitna quantity move hui.
      - **Example**: `5.00`
  - `date` (Date)
      - **Why**: Kab hua.
      - **Example**: `2025-11-20`
  - `notes` (Text)
      - **Why**: Extra details.
      - **Example**: `"Used for lunch preparation"`
  - `recorded_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne entry ki.
      - **Example**: `Cook ka user_id`

-----



## 💼 MODULE 11: PAYROLL MANAGEMENT (App: `payroll`)

### Purpose: Staff Ki Salary Ka Hisab

Cook, guard, cleaner - sabki attendance aur payment.

#### 11.1 Table: `StaffAttendance`

**Description**: Daily attendance register for staff.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har attendance record ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440060`
  - `staff_id` (Foreign Key -> CustomUser)
      - **Why (Advanced Feature 3)**: Kaunse staff member ka attendance hai.
      - **Example**: `Cook ka user_id`
  - `date` (Date)
      - **Why**: Kaunse din ka attendance hai.
      - **Example**: `2025-11-20`
  - `status` (Enum: PRESENT, ABSENT, HALF_DAY, LEAVE)
      - **Why**: Us din kaam par aaya ya nahi.
      - **Example**: `PRESENT`
  - `check_in_time` (Time, Nullable)
      - **Why**: Kitne baje aaya.
      - **Example**: `08:30:00`
  - `check_out_time` (Time, Nullable)
      - **Why**: Kitne baje gaya.
      - **Example**: `18:00:00`
  - `selfie_photo` (Image, Nullable)
      - **Why (Advanced Feature 3)**: Biometric attendance ke liye selfie.
      - **Example**: `staff_attendance/cook_20nov.jpg`
  - `notes` (Text)
      - **Why**: Extra remarks (e.g., "Half day due to medical").
      - **Example**: `"Left early for doctor appointment"`

**Unique Constraint**: (staff, date) - Ek staff ka ek din mein sirf ek record

#### 11.2 Table: `SalaryPayment`

**Description**: Monthly salary records.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har salary payment ko track karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440061`
  - `staff_id` (Foreign Key -> CustomUser)
      - **Why**: Kisko salary di gayi.
      - **Example**: `Cook ka user_id`
  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse PG ki salary hai.
      - **Example**: `Property ka UUID`
  - `month` (Date)
      - **Why**: Kaunse mahine ki salary hai (month ka first day).
      - **Example**: `2025-11-01`
  - `days_worked` (Decimal)
      - **Why**: Kitne din kaam kiya (attendance se calculate).
      - **Example**: `26.5` (26 full days + 1 half day)
  - `daily_rate` (Decimal)
      - **Why**: Per day kitna milta hai.
      - **Example**: `500.00`
  - `gross_salary` (Decimal)
      - **Why**: Total salary before deductions (days_worked * daily_rate).
      - **Example**: `13250.00`
  - `deductions` (Decimal)
      - **Why**: Koi advance liya tha ya fine laga.
      - **Example**: `500.00`
  - `net_salary` (Decimal)
      - **Why**: Final amount jo diya gaya (gross - deductions).
      - **Example**: `12750.00`
  - `payment_date` (Date)
      - **Why**: Kab salary di gayi.
      - **Example**: `2025-12-01`
  - `payment_mode` (Enum: CASH, BANK, UPI)
      - **Why**: Kaise payment kiya.
      - **Example**: `BANK`
  - `transaction_reference` (String, Nullable)
      - **Why**: Bank transfer ka reference number.
      - **Example**: `"UTR123456789"`

**Unique Constraint**: (staff, month) - Ek staff ko ek mahine mein sirf ek salary

-----

## 🧹 MODULE 12: HYGIENE MANAGEMENT (App: `hygiene`)

### Purpose: Safai Ka Score

Weekly inspection aur public rating.

#### 12.1 Table: `HygieneInspection`

**Description**: Weekly hygiene inspection records.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har inspection ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440070`
  - `property_id` (Foreign Key -> Property)
      - **Why (USP 13)**: Kaunse PG ka inspection hai.
      - **Example**: `Property ka UUID`
  - `inspection_date` (Date)
      - **Why**: Kab inspection hua.
      - **Example**: `2025-11-20`
  - `inspector_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne inspection kiya (Manager/SuperAdmin).
      - **Example**: `Manager ka user_id`
  - `cleanliness_score` (Integer)
      - **Why**: General cleanliness ka score (out of 10).
      - **Example**: `8`
  - `kitchen_score` (Integer)
      - **Why**: Kitchen ki safai ka score (out of 10).
      - **Example**: `9`
  - `bathroom_score` (Integer)
      - **Why**: Bathrooms ki safai ka score (out of 10).
      - **Example**: `7`
  - `common_area_score` (Integer)
      - **Why**: Common areas ka score (out of 10).
      - **Example**: `8`
  - `overall_rating` (Decimal)
      - **Why**: Average rating out of 5 (public display ke liye).
      - **Example**: `4.00`
  - `photos` (JSON)
      - **Why**: Inspection photos ka list.
      - **Example**: `["hygiene/kitchen1.jpg", "hygiene/bathroom1.jpg"]`
  - `remarks` (Text)
      - **Why**: Inspector ke comments.
      - **Example**: `"Kitchen needs deep cleaning"`

-----

## ⭐ MODULE 13: FEEDBACK MANAGEMENT (App: `feedback`)

### Purpose: Quality Control

Complaints aur mess food ka rating.

#### 13.1 Table: `ComplaintFeedback`

**Description**: Feedback on resolved complaints.
**Fields**:

  - `complaint_id` (Foreign Key -> Complaint, Primary Key)
      - **Why (Technical Feature 9)**: Kaunsi complaint ka feedback hai.
      - **Example**: `Complaint ka UUID`
  - `rating` (Integer)
      - **Why**: Manager ne kitna achha kaam kiya (1-5).
      - **Example**: `4`
  - `feedback_text` (Text)
      - **Why**: Student ke comments.
      - **Example**: `"Fixed quickly but plumber was rude"`
  - `submitted_at` (DateTime)
      - **Why**: Kab feedback diya.
      - **Example**: `2025-11-20T16:00:00Z`

#### 13.2 Table: `MessFeedback`

**Description**: Daily mess food ratings.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har feedback ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440080`
  - `tenant_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne feedback diya.
      - **Example**: `Rahul ka user_id`
  - `menu_id` (Foreign Key -> MessMenu)
      - **Why**: Kaunse din ke khane ka feedback hai.
      - **Example**: `Menu ka UUID`
  - `meal_type` (Enum: BREAKFAST, LUNCH, DINNER)
      - **Why**: Kaunsa meal tha.
      - **Example**: `LUNCH`
  - `rating` (Integer)
      - **Why**: Khana kaisa tha (1-5).
      - **Example**: `3`
  - `feedback_text` (Text)
      - **Why**: Student ke comments.
      - **Example**: `"Dal was too salty"`
  - `submitted_at` (DateTime)
      - **Why**: Kab feedback diya.
      - **Example**: `2025-11-20T14:30:00Z`

-----

## 🕵️ MODULE 14: AUDIT LOGS (App: `audit`)

### Purpose: Chori Pakadna

Har action ka record - fraud detection ke liye.

#### 14.1 Table: `AuditLog`

**Description**: Complete activity trail.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har action ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440090`
  - `user_id` (Foreign Key -> CustomUser, Nullable)
      - **Why (Technical Feature 7)**: Kisne action kiya.
      - **Example**: `Manager ka user_id`
  - `action_type` (Enum: CREATE, UPDATE, DELETE, LOGIN, LOGOUT, PAYMENT, REFUND)
      - **Why**: Kya action hua.
      - **Example**: `DELETE`
  - `model_name` (String)
      - **Why**: Kaunsi table affect hui.
      - **Example**: `"Transaction"`
  - `object_id` (String)
      - **Why**: Kaunsa record affect hua.
      - **Example**: `"550e8400-e29b-41d4-a716-446655440100"`
  - `changes` (JSON)
      - **Why**: Kya change hua (before/after values).
      - **Example**: `{"amount": {"old": "5000", "new": "0"}}`
  - `ip_address` (IP Address, Nullable)
      - **Why**: Kahan se action hua.
      - **Example**: `"192.168.1.100"`
  - `timestamp` (DateTime)
      - **Why**: Kab hua.
      - **Example**: `2025-11-20T22:05:00Z`

-----

## 🎓 MODULE 15: ALUMNI NETWORK (App: `alumni`)

### Purpose: Ex-Students Ka Network

Job referrals aur networking.

#### 15.1 Table: `AlumniProfile`

**Description**: Ex-tenant profiles.
**Fields**:

  - `user_id` (Foreign Key -> CustomUser, Primary Key)
      - **Why (Advanced Feature 9)**: Kaunsa ex-student hai.
      - **Example**: `Rahul ka user_id`
  - `current_company` (String, Nullable)
      - **Why**: Abhi kahan kaam karta hai.
      - **Example**: `"Google India"`
  - `current_position` (String, Nullable)
      - **Why**: Kya position hai.
      - **Example**: `"Software Engineer"`
  - `linkedin_url` (URL, Nullable)
      - **Why**: LinkedIn profile link.
      - **Example**: `"https://linkedin.com/in/rahul123"`
  - `is_open_to_referrals` (Boolean)
      - **Why**: Kya wo referrals dene ke liye ready hai.
      - **Example**: `True`
  - `exit_date` (Date)
      - **Why**: PG kab chhoda tha.
      - **Example**: `2024-06-30`
  - `properties_stayed` (ManyToMany -> Property)
      - **Why**: Kaunse PGs mein raha tha.
      - **Example**: `[Property1_UUID, Property2_UUID]`

#### 15.2 Table: `JobReferral`

**Description**: Referral requests between alumni and current tenants.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har referral request ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440110`
  - `requester_id` (Foreign Key -> CustomUser)
      - **Why**: Kisne referral manga.
      - **Example**: `Current tenant ka user_id`
  - `alumni_id` (Foreign Key -> CustomUser)
      - **Why**: Kisse referral manga.
      - **Example**: `Alumni ka user_id`
  - `company_name` (String)
      - **Why**: Kaunsi company ke liye referral chahiye.
      - **Example**: `"Amazon"`
  - `position` (String)
      - **Why**: Kaunsi position ke liye.
      - **Example**: `"SDE Intern"`
  - `message` (Text)
      - **Why**: Requester ka message.
      - **Example**: `"Hi, I'm applying for SDE role. Can you refer me?"`
  - `status` (Enum: REQUESTED, ACCEPTED, REJECTED, COMPLETED)
      - **Why**: Request ka current state.
      - **Example**: `ACCEPTED`
  - `created_at` (DateTime)
      - **Why**: Kab request bheji.
      - **Example**: `2025-11-20T10:00:00Z`
  - `updated_at` (DateTime)
      - **Why**: Last kab update hua.
      - **Example**: `2025-11-21T15:00:00Z`

-----

## 💼 MODULE 16: SAAS SUBSCRIPTION (App: `saas`)

### Purpose: Software Bechna

Agar aap ye software doosre PG owners ko bechenge.

#### 16.1 Table: `SubscriptionPlan`

**Description**: Different pricing tiers.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har plan ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440120`
  - `name` (String)
      - **Why (Technical Feature 8)**: Plan ka naam.
      - **Example**: `"Gold Plan"`
  - `price_per_month` (Decimal)
      - **Why**: Monthly subscription cost.
      - **Example**: `2999.00`
  - `max_properties` (Integer)
      - **Why**: Kitne PG branches allow hain.
      - **Example**: `3`
  - `max_rooms` (Integer)
      - **Why**: Total kitne rooms allow hain.
      - **Example**: `50`
  - `features` (JSON)
      - **Why**: Kaunse features enabled hain.
      - **Example**: `{"crm": true, "alumni": false, "reports": true}`
  - `is_active` (Boolean)
      - **Why**: Plan abhi available hai ya nahi.
      - **Example**: `True`

#### 16.3 Table: `AppVersion`

**Description**: Force update logic.
**Fields**:

  - `platform` (Enum: ANDROID, IOS)
      - **Why**: OS type.
  - `version_code` (Integer)
      - **Why**: Internal version (102).
  - `version_name` (String)
      - **Why**: Public version (1.0.2).
  - `is_mandatory` (Boolean)
      - **Why**: Force update?


#### 16.2 Table: `PropertySubscription`

**Description**: Owner's subscription status.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har subscription ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440121`
  - `owner_id` (Foreign Key -> CustomUser)
      - **Why**: Kaunse owner ka subscription hai.
      - **Example**: `SuperAdmin ka user_id`
  - `plan_id` (Foreign Key -> SubscriptionPlan)
      - **Why**: Kaunsa plan liya hai.
      - **Example**: `Gold Plan ka UUID`
  - `status` (Enum: ACTIVE, EXPIRED, CANCELLED, TRIAL)
      - **Why**: Subscription ka current state.
      - **Example**: `ACTIVE`
  - `start_date` (Date)
      - **Why**: Kab shuru hua.
      - **Example**: `2025-11-01`
  - `end_date` (Date)
      - **Why**: Kab expire hoga.
      - **Example**: `2025-12-01`
  - `auto_renew` (Boolean)
      - **Why**: Automatic renew hoga ya nahi.
      - **Example**: `True`

-----

## 📊 MODULE 17: REPORTS & ANALYTICS (App: `reports`)

### Purpose: Data Download Karna

Excel/PDF reports generate karna.

#### 17.1 Table: `GeneratedReport`

**Description**: Stored report files.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har report ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440130`
  - `property_id` (Foreign Key -> Property, Nullable)
      - **Why (Advanced Feature 8)**: Kaunse PG ki report hai (null = all properties).
      - **Example**: `Property ka UUID`
  - `report_type` (Enum: MONTHLY_RENT, EXPENSE, GST, OCCUPANCY, STAFF_PAYROLL)
      - **Why**: Kaunsi type ki report hai.
      - **Example**: `MONTHLY_RENT`
  - `generated_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne generate kiya.
      - **Example**: `SuperAdmin ka user_id`
  - `file` (File)
      - **Why**: Actual Excel/PDF file.
      - **Example**: `reports/rent_nov2025.xlsx`
  - `start_date` (Date)
      - **Why**: Report ka start period.
      - **Example**: `2025-11-01`
  - `end_date` (Date)
      - **Why**: Report ka end period.
      - **Example**: `2025-11-30`
  - `created_at` (DateTime)
      - **Why**: Kab generate hua.
      - **Example**: `2025-12-01T10:00:00Z`

-----

## 📋 ADDITIONAL FIELDS IN EXISTING MODELS

### Property Model (Updated)

**New Fields Added**:

  - `current_hygiene_rating` (Decimal)
      - **Why (USP 13)**: Public display ke liye current hygiene score.
      - **Example**: `4.50`
  - `preferred_language` (Enum: EN, HI, TE)
      - **Why (Technical Feature 6)**: Staff ke liye language preference.
      - **Example**: `HI`
  - `is_active` (Boolean)
      - **Why**: Property operational hai ya band hai.
      - **Example**: `True`
  - `created_at` (DateTime)
      - **Why**: Property kab add hui.
      - **Example**: `2025-01-01T00:00:00Z`
  - `updated_at` (DateTime)
      - **Why**: Last kab update hui.
      - **Example**: `2025-11-20T10:00:00Z`

### Room Model (Updated)

**New Fields Added**:

  - `has_ac` (Boolean)
      - **Why**: AC hai ya nahi - filtering ke liye.
      - **Example**: `True`
  - `has_balcony` (Boolean)
      - **Why**: Balcony hai ya nahi.
      - **Example**: `False`
  - `has_attached_bathroom` (Boolean)
      - **Why**: Attached bathroom hai ya common.
      - **Example**: `True`
  - `floor_number` (Integer)
      - **Why**: Kaunsi floor par hai.
      - **Example**: `2`

### Booking Model (Updated)

**New Fields Added**:

  - `fintech_partner_name` (String, Nullable)
      - **Why (USP 8)**: Kaunsi loan company se zero deposit liya.
      - **Example**: `"PayLater Finance"`
  - `fintech_loan_id` (String, Nullable)
      - **Why**: Loan ka reference ID.
      - **Example**: `"LOAN123456"`
  - `refund_amount` (Decimal, Nullable)
      - **Why (USP 9)**: Exit time kitna refund dena hai.
      - **Example**: `15500.00`
  - `refund_processed_date` (Date, Nullable)
      - **Why**: Refund kab process hua.
      - **Example**: `2025-11-25`

### EntryLog Model (Updated)

**New Fields Added**:

  - `property_id` (Foreign Key -> Property)
      - **Why**: Kaunse PG ka entry log hai.
      - **Example**: `Property ka UUID`
  - `entry_method` (Enum: BIOMETRIC, QR, MANUAL)
      - **Why (USP 12)**: Kaise entry hui.
      - **Example**: `BIOMETRIC`

-----

## 🌍 MODULE 18: LOCALIZATION & LANGUAGE SUPPORT (App: `localization`)

### Purpose: Multi-Language System

Staff (Cook/Guard) ko Hindi chahiye, Parents ko regional languages - sabke liye translation system.

#### 18.1 Table: `TranslationString`

**Description**: Stores UI translations for all app modules in multiple languages.
**Fields**:

  - `id` (UUID, Primary Key)
      - **Why**: Har translation entry ko identify karne ke liye.
      - **Example**: `550e8400-e29b-41d4-a716-446655440140`
  - `module` (String)
      - **Why (Technical Feature 6)**: Kaunse app module ka translation hai (mess, payroll, finance etc.).
      - **Example**: `"payroll"`
  - `key` (String)
      - **Why**: Translation key - code mein kaunsa string use ho raha hai.
      - **Example**: `"mark_attendance"`
  - `language` (Enum: en, hi, ta, te, kn, bn)
      - **Why**: Target language code.
      - **Example**: `hi` (Hindi)
      - **Choices**: English (en), Hindi (hi), Tamil (ta), Telugu (te), Kannada (kn), Bengali (bn)
  - `value` (Text)
      - **Why**: Actual translated text.
      - **Example**: `"हाजिरी लगाएं"` (Mark Attendance in Hindi)
  - `created_at` (DateTime)
      - **Why**: Kab translation add hui.
      - **Example**: `2025-11-01T10:00:00Z`
  - `updated_at` (DateTime)
      - **Why**: Last kab update hui.
      - **Example**: `2025-11-20T15:00:00Z`
  - `updated_by_id` (Foreign Key -> CustomUser, Nullable)
      - **Why**: Kisne update kiya (SuperAdmin).
      - **Example**: `Admin ka user_id`

**Unique Constraint**: (module, key, language) - Ek module ke ek key ka ek language mein sirf ek translation

**Use Cases**:
- Staff app mein button "Mark Attendance" ki jagah "हाजिरी लगाएं" dikhe
- Parent portal mein "Your son entered PG" ki jagah regional language mein message
- Mess app mein "Book Meal" ki jagah "खाना बुक करें" dikhe

-----

## 📊 FINAL SUMMARY: COMPLETE DATABASE STRUCTURE

### Total Apps: 18

| # | App Name | Purpose | Models Count |
|---|----------|---------|--------------|
| 1 | users | Authentication & Profiles | 3 |
| 2 | properties | PG Branches, Rooms, Beds, Assets | 7 |
| 3 | bookings | Booking & Digital Agreements | 2 |
| 4 | finance | Invoices, Transactions, Expenses | 3 |
| 5 | operations | Complaints, Entry Logs, Notices, ChatLog | 4 |
| 6 | mess | Menu & Meal Selections | 2 |
| 7 | crm | Lead Management | 1 |
| 8 | notifications | Alerts & FCM Tokens | 2 |
| 9 | visitors | Visitor Management | 1 |
| 10 | inventory | Stock Management | 2 |
| 11 | payroll | Staff Attendance & Salary | 2 |
| 12 | hygiene | Hygiene Inspections | 1 |
| 13 | feedback | Ratings & Reviews | 2 |
| 14 | audit | Activity Logs | 1 |
| 15 | alumni | Alumni Network & Referrals | 2 |
| 16 | saas | Subscription Plans & Versioning | 3 |
| 17 | reports | Generated Reports | 1 |
| 18 | localization | Multi-Language Translations | 1 |
| **TOTAL** | | | **40+ Models** |

### Feature Coverage: 100% ✅

✅ **All 6 Core Modules** - Fully Covered
✅ **All 15 USP Features** - Fully Covered (including AI Compatibility with detailed preferences)
✅ **All 9 Advanced Features** - Fully Covered
✅ **All 9 Technical Features** - Fully Covered (including Multi-Language Support)

### Key Highlights:

1. **UUID Primary Keys**: Security aur scalability ke liye
2. **Foreign Keys**: Proper relationships between tables
3. **Enums**: Data consistency ke liye predefined choices
4. **JSON Fields**: Flexibility ke liye (lifestyle_attributes, features, photos)
5. **Timestamps**: Audit trail ke liye created_at/updated_at
6. **Nullable Fields**: Optional data ke liye
7. **Unique Constraints**: Duplicate data prevent karne ke liye
8. **Multi-Language Support**: 6 languages ke liye complete translation system
9. **AI Matching**: Detailed preference fields for accurate roommate compatibility

### Database Design Principles Followed:

- **Normalization**: No data redundancy
- **Scalability**: Multi-property support from day 1
- **Audit Trail**: Har important action logged hai
- **Flexibility**: JSON fields for future extensions
- **Performance**: Proper indexing (db_index=True on frequently queried fields)
- **Internationalization**: Built-in support for 6 languages
- **AI-Ready**: Structured data fields for machine learning algorithms

### Latest Updates (Version 2.0):

1. **Localization Support**: Added `preferred_language` to CustomUser and complete TranslationString model
2. **Enhanced AI Matching**: Replaced generic JSON with structured fields (sleep_schedule, cleanliness_level, noise_tolerance, study_hours)
3. **Consistent Naming**: Renamed tenants app to bookings throughout
4. **Complete Coverage**: All 33 features from Project_Summary_Features.md now fully supported

---

**🎯 Ab ye database design 100% production-ready aur completely aligned hai!**

Har field ka purpose crystal clear hai, har USP supported hai with proper field definitions, aur koi confusion nahi hai. Beginner bhi easily samajh sakta hai ki kaunsa field kyun hai aur kaise use hoga.

**Alignment Status**:
✅ Project_Summary_Features.md - 100% Aligned
✅ All_Database_Tables_Models.md - 100% Aligned  
✅ All_Services_Documentation.md - 100% Aligned

**Next Step**: Django models.py files create karna aur migrations run karna! 🚀

---

**📝 Document Version:** 2.0 (Complete & Fully Aligned)  
**📅 Last Updated:** December 2025  
**🎯 Total Models:** 40+ across 18 Django apps  
**✅ Feature Coverage:** 33/33 Features (100%)
