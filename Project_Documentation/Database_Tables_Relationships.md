# 🔗 Database Tables Relationships & Associations

This document provides a **complete and exhaustive** guide to how database tables (models) are connected in the **Smart PG Management System**. It covers every single relationship defined in the codebase, ensuring new developers have 100% clarity on the data architecture.

---

## 🏗️ Legend & Concepts

### Relationship Types Explained:

*   **One-to-One (1:1):** One record in Table A is linked to exactly one record in Table B.
    *   *Symbol:* `1 -- 1`
    *   *Real Example:* One User has exactly one TenantProfile. One TenantProfile belongs to exactly one User.
    *   *Django Implementation:* `OneToOneField`
    *   *Database Level:* Foreign key with UNIQUE constraint

*   **One-to-Many (1:N):** One record in Table A is linked to multiple records in Table B.
    *   *Symbol:* `1 -- N`
    *   *Real Example:* One Property can have many Rooms. Each Room belongs to exactly one Property.
    *   *Django Implementation:* `ForeignKey` on the "Many" side
    *   *Database Level:* Foreign key column

*   **Many-to-Many (M:N):** Multiple records in Table A are linked to multiple records in Table B.
    *   *Symbol:* `N -- N`
    *   *Real Example:* One User can have multiple FCM tokens (different devices). One device can be used by multiple users (shared device).
    *   *Django Implementation:* `ManyToManyField` or through intermediate table
    *   *Database Level:* Junction/Bridge table with two foreign keys

### Key Database Concepts for New Developers:

1. **Foreign Key (FK):** A field that references the primary key of another table
2. **Primary Key (PK):** Unique identifier for each record in a table
3. **Cascade Delete:** When parent record is deleted, child records are also deleted
4. **Set NULL:** When parent record is deleted, child's foreign key becomes NULL
5. **Protect:** Prevents deletion of parent if child records exist

---

## 1. 👤 `users` App Relationships

### `CustomUser` - The Central Authentication Hub
**Purpose:** This is the core user table that handles authentication and basic user information for all user types (SuperAdmin, Manager, Tenant, Parent, Staff).

**Key Characteristics:**
- Uses Django's AbstractUser as base (inherits username, email, password fields)
- Has a `role` field to distinguish user types
- Uses UUID as primary key for better security
- Referenced by almost every other table in the system

**Real-World Scenario:**
```
User ID: 123e4567-e89b-12d3-a456-426614174000
Username: "rahul_sharma"
Role: "TENANT"
Phone: "+91-9876543210"
```

### `TenantProfile` - Extended Student Information
**Purpose:** Stores additional information specific to students/tenants that regular users don't need.

#### Relationships:

**1. `TenantProfile` ↔ `CustomUser` (user) - 1:1 Relationship**
- **Field:** `user = OneToOneField(CustomUser)`
- **Meaning:** Each tenant profile is linked to exactly one user account
- **Real Example:** 
  ```
  CustomUser: rahul_sharma (ID: 123)
  TenantProfile: Aadhaar=1234-5678-9012, Credit Score=750 (user_id: 123)
  ```
- **Database Behavior:** If CustomUser is deleted, TenantProfile is also deleted (CASCADE)
- **Why This Design:** Separates authentication data from tenant-specific data for better organization

**2. `TenantProfile` ↔ `CustomUser` (guardian) - N:1 Relationship**
- **Field:** `guardian = ForeignKey(CustomUser, related_name='wards')`
- **Meaning:** Multiple tenants can have the same guardian (parent)
- **Real Example:**
  ```
  Parent: Mr. Sharma (ID: 456, Role: PARENT)
  Tenant 1: Rahul (guardian_id: 456)
  Tenant 2: Priya (guardian_id: 456)  # Same parent, different children
  ```
- **Business Logic:** Enables parent portal access where parents can monitor multiple children
- **Database Behavior:** If parent is deleted, guardian field becomes NULL (SET_NULL)

### `StaffProfile` - Employee Information
**Purpose:** Stores employment details for staff members (Cook, Guard, Cleaner, etc.)

#### Relationships:

**1. `StaffProfile` ↔ `CustomUser` (user) - 1:1 Relationship**
- **Field:** `user = OneToOneField(CustomUser)`
- **Meaning:** Each staff profile belongs to exactly one user account
- **Real Example:**
  ```
  CustomUser: ramu_cook (ID: 789, Role: STAFF)
  StaffProfile: Role=COOK, Daily Rate=₹500 (user_id: 789)
  ```
- **Why This Design:** Keeps staff-specific data (salary, role) separate from login credentials

**2. `StaffProfile` ↔ `Property` (assigned_property) - N:1 Relationship**
- **Field:** `assigned_property = ForeignKey(Property)`
- **Meaning:** Multiple staff members can work at the same property
- **Real Example:**
  ```
  Property: Gokuldham PG (ID: 101)
  Staff 1: Ramu (Cook, property_id: 101)
  Staff 2: Shyam (Guard, property_id: 101)
  Staff 3: Rita (Cleaner, property_id: 101)
  ```
- **Business Logic:** Enables property-wise staff management and payroll calculation

---

## 2. 🏨 `properties` App Relationships

### `Property` - PG Branch/Location
**Purpose:** Represents a physical PG building/branch. This is the central entity for multi-property management.

#### Relationships:

**1. `Property` ↔ `CustomUser` (owner) - N:1 Relationship**
- **Field:** `owner = ForeignKey(CustomUser, limit_choices_to={'role': 'SUPERADMIN'})`
- **Meaning:** One owner can have multiple properties, but each property has one owner
- **Real Example:**
  ```
  Owner: Mr. Gupta (SuperAdmin)
  Property 1: Gokuldham PG, Andheri (owner_id: Mr. Gupta)
  Property 2: Sunrise PG, Bandra (owner_id: Mr. Gupta)
  Property 3: Comfort PG, Malad (owner_id: Mr. Gupta)
  ```
- **Business Logic:** Enables multi-property business management under single ownership

**2. `Property` ↔ `CustomUser` (manager) - N:1 Relationship**
- **Field:** `manager = ForeignKey(CustomUser, limit_choices_to={'role': 'MANAGER'})`
- **Meaning:** One manager can handle multiple properties, each property has one assigned manager
- **Real Example:**
  ```
  Manager: Rajesh (Manager)
  Property 1: Gokuldham PG (manager_id: Rajesh)
  Property 2: Sunrise PG (manager_id: Rajesh)  # Same manager for multiple properties
  ```
- **Business Logic:** Allows flexible manager assignment and workload distribution

### `Room` - Physical Rooms in PG
**Purpose:** Represents individual rooms within a property (Room 101, 102, etc.)

#### Relationships:

**1. `Room` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Multiple rooms belong to one property
- **Real Example:**
  ```
  Property: Gokuldham PG (ID: 101)
  Room 1: Room 101 (property_id: 101, capacity: 2, has_ac: True)
  Room 2: Room 102 (property_id: 101, capacity: 3, has_ac: False)
  Room 3: Room 103 (property_id: 101, capacity: 2, has_balcony: True)
  ```
- **Database Constraint:** `unique_together = ('property', 'room_number')` prevents duplicate room numbers in same property
- **Business Logic:** Enables room inventory management per property

### `PricingRule` - Dynamic Pricing System
**Purpose:** Implements seasonal/demand-based pricing (USP 4: Dynamic Pricing Engine)

#### Relationships:

**1. `PricingRule` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each property can have multiple pricing rules for different seasons
- **Real Example:**
  ```
  Property: Gokuldham PG
  Rule 1: Summer Surge (June-August, 1.15x multiplier)
  Rule 2: Festival Premium (October-November, 1.10x multiplier)
  Rule 3: Winter Discount (December-February, 0.90x multiplier)
  ```
- **Business Logic:** Automatic rent calculation based on current month and applicable rules

### `Bed` - Individual Bed Units
**Purpose:** The smallest bookable unit. Each bed can be occupied by one tenant.

#### Relationships:

**1. `Bed` ↔ `Room` (room) - N:1 Relationship**
- **Field:** `room = ForeignKey(Room)`
- **Meaning:** Multiple beds exist in one room
- **Real Example:**
  ```
  Room: 101 (Capacity: 2)
  Bed 1: Bed A (room_id: 101, is_occupied: True)
  Bed 2: Bed B (room_id: 101, is_occupied: False)
  ```
- **Database Constraint:** `unique_together = ('room', 'bed_label')` prevents duplicate bed labels in same room
- **Business Logic:** Enables bed-level booking and occupancy tracking

### `ElectricityReading` - IoT Meter Data
**Purpose:** Stores individual electricity consumption per bed (USP 5: Smart Electricity Billing)

#### Relationships:

**1. `ElectricityReading` ↔ `Bed` (bed) - N:1 Relationship**
- **Field:** `bed = ForeignKey(Bed)`
- **Meaning:** Each bed can have multiple electricity readings over time
- **Real Example:**
  ```
  Bed: Room 101-A
  Reading 1: 45.2 kWh (Jan 1, 2024)
  Reading 2: 52.8 kWh (Jan 2, 2024)
  Reading 3: 48.1 kWh (Jan 3, 2024)
  ```
- **Business Logic:** Enables fair electricity billing based on individual consumption

### `Asset` - Property Equipment
**Purpose:** Manages physical assets like ACs, geysers, furniture (Advanced Feature 4: Asset Management)

#### Relationships:

**1. `Asset` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** All assets belong to a specific property
- **Real Example:**
  ```
  Property: Gokuldham PG
  Asset 1: 1.5 Ton AC (QR: AC001, Room: 101)
  Asset 2: Water Heater (QR: WH002, Room: 102)
  Asset 3: WiFi Router (QR: RT003, Common Area)
  ```

**2. `Asset` ↔ `Room` (room) - N:1 Relationship (Optional)**
- **Field:** `room = ForeignKey(Room, null=True, blank=True)`
- **Meaning:** Assets can be room-specific or common area assets
- **Business Logic:** Enables location-based asset tracking and maintenance scheduling

### `AssetServiceLog` - Maintenance History
**Purpose:** Tracks all repairs and maintenance done on assets

#### Relationships:

**1. `AssetServiceLog` ↔ `Asset` (asset) - N:1 Relationship**
- **Field:** `asset = ForeignKey(Asset)`
- **Meaning:** Each asset can have multiple service records
- **Real Example:**
  ```
  Asset: AC in Room 101
  Service 1: Gas refill (₹2000, Jan 15, 2024)
  Service 2: Filter cleaning (₹500, Feb 20, 2024)
  Service 3: Compressor repair (₹5000, Mar 10, 2024)
  ```
- **Business Logic:** Enables service history tracking and predictive maintenance

---

## 3. 📅 `bookings` App Relationships

### `Booking` - Tenant Stay Management
**Purpose:** Central table that manages a tenant's entire lifecycle in the PG (check-in to check-out)

#### Relationships:

**1. `Booking` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** One tenant can have multiple bookings (different time periods or properties)
- **Real Example:**
  ```
  Tenant: Rahul Sharma
  Booking 1: Gokuldham PG, Room 101-A (Jan 2024 - Jun 2024) [EXITED]
  Booking 2: Sunrise PG, Room 205-B (Jul 2024 - Present) [ACTIVE]
  ```
- **Business Logic:** Enables booking history tracking and re-bookings
- **Database Behavior:** PROTECT prevents accidental tenant deletion if active bookings exist

**2. `Booking` ↔ `Bed` (bed) - N:1 Relationship**
- **Field:** `bed = ForeignKey(Bed)`
- **Meaning:** Multiple bookings can be made for the same bed over time (different tenants)
- **Real Example:**
  ```
  Bed: Room 101-A
  Booking 1: Rahul (Jan-Jun 2024) [EXITED]
  Booking 2: Amit (Jul-Dec 2024) [ACTIVE]
  Booking 3: Priya (Jan 2025 onwards) [Future booking]
  ```
- **Business Logic:** Enables bed occupancy history and future booking management

### `DigitalAgreement` - E-Signed Contracts
**Purpose:** Stores digitally signed rental agreements (USP 7: Digital Agreement)

#### Relationships:

**1. `DigitalAgreement` ↔ `Booking` (booking) - 1:1 Relationship**
- **Field:** `booking = OneToOneField(Booking, primary_key=True)`
- **Meaning:** Each booking has exactly one rental agreement
- **Real Example:**
  ```
  Booking: Rahul in Room 101-A (ID: 12345)
  Agreement: rental_agreement_12345.pdf (signed: True, signed_at: Jan 1, 2024)
  ```
- **Business Logic:** Legal compliance and paperless documentation

---

## 4. 💸 `finance` App Relationships

### `Invoice` - Monthly Bills
**Purpose:** Generates monthly bills for tenants including rent, mess charges, electricity, etc.

#### Relationships:

**1. `Invoice` ↔ `Booking` (booking) - N:1 Relationship**
- **Field:** `booking = ForeignKey(Booking)`
- **Meaning:** Each booking can have multiple invoices (monthly bills)
- **Real Example:**
  ```
  Booking: Rahul in Room 101-A (6-month stay)
  Invoice 1: January 2024 (Rent: ₹8000, Mess: ₹3000, Electricity: ₹500)
  Invoice 2: February 2024 (Rent: ₹8000, Mess: ₹2800, Electricity: ₹600)
  Invoice 3: March 2024 (Rent: ₹8000, Mess: ₹3200, Electricity: ₹450)
  ```
- **Business Logic:** Automated monthly billing with itemized charges

### `Transaction` - Financial Movement Log
**Purpose:** Records all money movements in the system (payments, refunds, expenses, salaries)

#### Relationships:

**1. `Transaction` ↔ `CustomUser` (user) - N:1 Relationship**
- **Field:** `user = ForeignKey(CustomUser)`
- **Meaning:** Each transaction is associated with a user (who paid/received money)

**2. `Transaction` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each transaction affects a specific property's finances

**3. `Transaction` ↔ `Invoice` (invoice) - N:1 Relationship (Optional)**
- **Field:** `invoice = ForeignKey(Invoice, null=True, blank=True)`
- **Meaning:** Some transactions are linked to specific invoices (bill payments)

### `Expense` - Operational Costs
**Purpose:** Tracks all business expenses for profit calculation

#### Relationships:

**1. `Expense` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each expense is recorded against a specific property

---

## 5. 🛠️ `operations` App Relationships

### `Complaint` - Issue Management System
**Purpose:** Handles tenant complaints and maintenance requests with tracking and resolution

#### Relationships:

**1. `Complaint` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** One tenant can raise multiple complaints

**2. `Complaint` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each complaint is specific to a property location

### `EntryLog` - Security & Safety Tracking
**Purpose:** Records all entry/exit activities for safety and parent monitoring

#### Relationships:

**1. `EntryLog` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant has multiple entry/exit records

**2. `EntryLog` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Tracks which property gate was used

### `Notice` - Communication System
**Purpose:** Digital notice board for property-wide announcements

#### Relationships:

**1. `Notice` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each notice is specific to a property

### `ChatLog` - AI Assistant Interactions
**Purpose:** Stores conversations between tenants and AI chatbot

#### Relationships:

**1. `ChatLog` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant has their own chat history with the bot

### `SOSAlert` - Emergency Response System
**Purpose:** Handles panic button alerts for tenant safety

#### Relationships:

**1. `SOSAlert` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant can trigger multiple SOS alerts

**2. `SOSAlert` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Alert is associated with property for jurisdiction and response

**3. `SOSAlert` ↔ `CustomUser` (first_responder) - N:1 Relationship**
- **Field:** `first_responder = ForeignKey(CustomUser, related_name='responded_sos_alerts')`
- **Meaning:** Tracks which staff member responded first

---

## 6. 🍛 `mess` App Relationships

### `MessMenu` - Daily Food Menu
**Purpose:** Manages daily food menu and pricing for the smart mess system

#### Relationships:

**1. `MessMenu` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each property has its own daily menu
- **Database Constraint:** `unique_together = ('property', 'date')` ensures one menu per property per day

### `DailyMealSelection` - Pay-Per-Day Mess System
**Purpose:** Implements the revolutionary pay-per-day mess wallet system

#### Relationships:

**1. `DailyMealSelection` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant makes daily meal choices

**2. `DailyMealSelection` ↔ `MessMenu` (menu) - N:1 Relationship**
- **Field:** `menu = ForeignKey(MessMenu)`
- **Meaning:** Each selection is linked to a specific day's menu

---

## 7. 🤝 `crm` App Relationships

### `Lead` - Enquiry & Sales Management
**Purpose:** Manages potential tenant enquiries and conversion tracking

#### Relationships:

**1. `Lead` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each enquiry is for a specific PG branch

**2. `Lead` ↔ `CustomUser` (converted_tenant) - 1:1 Relationship (Optional)**
- **Field:** `converted_tenant = OneToOneField(CustomUser, null=True, blank=True)`
- **Meaning:** If lead converts to tenant, links to their user account

---

## 8. 🔔 `notifications` App Relationships

### `NotificationLog` - Communication Audit Trail
**Purpose:** Tracks all notifications sent to users for delivery confirmation and debugging

#### Relationships:

**1. `NotificationLog` ↔ `CustomUser` (user) - N:1 Relationship**
- **Field:** `user = ForeignKey(CustomUser)`
- **Meaning:** Each user receives multiple notifications over time

### `FCMToken` - Push Notification Infrastructure
**Purpose:** Manages Firebase Cloud Messaging tokens for real-time push notifications

#### Relationships:

**1. `FCMToken` ↔ `CustomUser` (user) - N:1 Relationship**
- **Field:** `user = ForeignKey(CustomUser)`
- **Meaning:** One user can have multiple devices (phone, tablet, web browser)

---

## 9. 🛑 `visitors` App Relationships

### `VisitorRequest` - Security & Guest Management
**Purpose:** Manages visitor entry approval system for enhanced security

#### Relationships:

**1. `VisitorRequest` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant can have multiple visitor requests

**2. `VisitorRequest` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each visit is specific to a property location

**3. `VisitorRequest` ↔ `CustomUser` (guard) - N:1 Relationship**
- **Field:** `guard = ForeignKey(CustomUser, limit_choices_to={'role': 'STAFF'})`
- **Meaning:** Tracks which security guard processed the visitor

---

## 10. 📦 `inventory` App Relationships

### `InventoryItem` - Kitchen Stock Management
**Purpose:** Tracks kitchen supplies and ingredients for mess operations

#### Relationships:

**1. `InventoryItem` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each property maintains its own kitchen inventory

### `InventoryTransaction` - Stock Movement Tracking
**Purpose:** Records all inventory movements for accurate stock tracking and cost analysis

#### Relationships:

**1. `InventoryTransaction` ↔ `InventoryItem` (item) - N:1 Relationship**
- **Field:** `item = ForeignKey(InventoryItem)`
- **Meaning:** Each item has multiple transactions over time

**2. `InventoryTransaction` ↔ `CustomUser` (recorded_by) - N:1 Relationship**
- **Field:** `recorded_by = ForeignKey(CustomUser)`
- **Meaning:** Tracks which staff member recorded the transaction

---

## 11. 👷 `payroll` App Relationships

### `StaffAttendance` - Employee Time Tracking
**Purpose:** Records daily attendance for all staff members with biometric/selfie verification

#### Relationships:

**1. `StaffAttendance` ↔ `CustomUser` (staff) - N:1 Relationship**
- **Field:** `staff = ForeignKey(CustomUser, limit_choices_to={'role': 'STAFF'})`
- **Meaning:** Each staff member has daily attendance records

### `SalaryPayment` - Automated Payroll System
**Purpose:** Calculates and records monthly salary payments based on attendance and daily rates

#### Relationships:

**1. `SalaryPayment` ↔ `CustomUser` (staff) - N:1 Relationship**
- **Field:** `staff = ForeignKey(CustomUser, limit_choices_to={'role': 'STAFF'})`
- **Meaning:** Each staff member receives monthly salary payments

**2. `SalaryPayment` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Salary is paid from specific property's account

---

## 12. 🧹 `hygiene` App Relationships

### `HygieneInspection` - Cleanliness Quality Control
**Purpose:** Implements systematic hygiene auditing for public rating and quality assurance

#### Relationships:

**1. `HygieneInspection` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each property undergoes regular hygiene inspections

**2. `HygieneInspection` ↔ `CustomUser` (inspector) - N:1 Relationship**
- **Field:** `inspector = ForeignKey(CustomUser, limit_choices_to={'role__in': ['MANAGER', 'SUPERADMIN']})`
- **Meaning:** Only managers and owners can conduct official inspections

---

## 13. ⭐ `feedback` App Relationships

### `ComplaintFeedback` - Service Quality Rating
**Purpose:** Collects tenant feedback on complaint resolution to improve service quality

#### Relationships:

**1. `ComplaintFeedback` ↔ `Complaint` (complaint) - 1:1 Relationship**
- **Field:** `complaint = OneToOneField(Complaint, primary_key=True)`
- **Meaning:** Each resolved complaint gets exactly one feedback rating

### `MessFeedback` - Food Quality Monitoring
**Purpose:** Daily food quality feedback to improve mess operations and menu planning

#### Relationships:

**1. `MessFeedback` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant can provide multiple food ratings

**2. `MessFeedback` ↔ `MessMenu` (menu) - N:1 Relationship**
- **Field:** `menu = ForeignKey(MessMenu)`
- **Meaning:** Each day's menu can receive multiple ratings from different tenants

---

## 14. 🕵️ `audit` App Relationships

### `AuditLog` - Security & Fraud Prevention
**Purpose:** Comprehensive activity tracking for security, compliance, and fraud detection

#### Relationships:

**1. `AuditLog` ↔ `CustomUser` (user) - N:1 Relationship**
- **Field:** `user = ForeignKey(CustomUser, null=True)`
- **Meaning:** Each action in the system is tracked with the user who performed it

---

## 🏁 Summary of Key Hubs

### 1. **`CustomUser`** - The Authentication & Identity Hub
**Why It's Central:** Every action in the system is performed by a user

**Connected To:**
- **Profiles:** TenantProfile, StaffProfile (identity extension)
- **Properties:** Property ownership and management
- **Bookings:** Tenant stays and reservations
- **Finance:** Transactions, invoices, salary payments
- **Operations:** Complaints, entry logs, SOS alerts, chat logs
- **Feedback:** Complaint ratings, mess reviews
- **Visitors:** Visitor requests and approvals
- **Inventory:** Stock transaction records
- **Payroll:** Staff attendance and salary
- **Hygiene:** Inspection records
- **Notifications:** SMS, email, push notification logs
- **Audit:** Activity tracking for security

### 2. **`Property`** - The Physical & Business Hub
**Why It's Central:** Represents the actual PG business location

**Connected To:**
- **Physical Structure:** Rooms, beds, assets
- **Business Rules:** Pricing rules, hygiene standards
- **Operations:** Staff assignment, expenses, notices
- **Customer Management:** Leads, visitor requests
- **Inventory:** Kitchen stock and supplies
- **Finance:** Property-wise profit/loss calculation
- **Safety:** SOS alert jurisdiction

### 3. **`Booking`** - The Business Transaction Hub
**Why It's Central:** Represents the core business transaction (tenant stay)

**Connected To:**
- **Revenue Generation:** Invoices and payments
- **Legal Compliance:** Digital agreements
- **Resource Allocation:** Bed occupancy
- **Customer Lifecycle:** Check-in to check-out journey

### 4. **Critical Relationships for New Developers:**

**Must Understand First:**
1. `CustomUser` → `TenantProfile` (1:1) - User identity
2. `Property` → `Room` → `Bed` (1:N:N) - Physical hierarchy
3. `Booking` → `CustomUser` + `Bed` (N:1 + N:1) - Business transaction
4. `Invoice` → `Booking` (N:1) - Revenue generation

**Advanced Relationships:**
5. `Transaction` → Multiple tables - Financial tracking
6. `SOSAlert` → Multiple users - Safety system
7. `Asset` → `AssetServiceLog` - Maintenance tracking) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** All assets belong to a specific property
- **Real Example:**
  ```
  Property: Gokuldham PG
  Asset 1: 1.5 Ton AC (QR: AC001, Room: 101)
  Asset 2: Water Heater (QR: WH002, Room: 102)
  Asset 3: WiFi Router (QR: RT003, Common Area)
  ```

**2. `Asset` ↔ `Room` (room) - N:1 Relationship (Optional)**
- **Field:** `room = ForeignKey(Room, null=True, blank=True)`
- **Meaning:** Assets can be room-specific or common area assets
- **Business Logic:** Enables location-based asset tracking and maintenance scheduling

### `AssetServiceLog` - Maintenance History
**Purpose:** Tracks all repairs and maintenance done on assets

#### Relationships:

**1. `AssetServiceLog` ↔ `Asset` (asset) - N:1 Relationship**
- **Field:** `asset = ForeignKey(Asset)`
- **Meaning:** Each asset can have multiple service records
- **Real Example:**
  ```
  Asset: AC in Room 101
  Service 1: Gas refill (₹2000, Jan 15, 2024)
  Service 2: Filter cleaning (₹500, Feb 20, 2024)
  Service 3: Compressor repair (₹5000, Mar 10, 2024)
  ```
- **Business Logic:** Enables service history tracking and predictive maintenance

---

## 3. 📅 `bookings` App Relationships

### `Booking` - Tenant Stay Management
**Purpose:** Central table that manages a tenant's entire lifecycle in the PG (check-in to check-out)

#### Relationships:

**1. `Booking` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** One tenant can have multiple bookings (different time periods or properties)
- **Real Example:**
  ```
  Tenant: Rahul Sharma
  Booking 1: Gokuldham PG, Room 101-A (Jan 2024 - Jun 2024) [EXITED]
  Booking 2: Sunrise PG, Room 205-B (Jul 2024 - Present) [ACTIVE]
  ```
- **Business Logic:** Enables booking history tracking and re-bookings
- **Database Behavior:** PROTECT prevents accidental tenant deletion if active bookings exist

**2. `Booking` ↔ `Bed` (bed) - N:1 Relationship**
- **Field:** `bed = ForeignKey(Bed)`
- **Meaning:** Multiple bookings can be made for the same bed over time (different tenants)
- **Real Example:**
  ```
  Bed: Room 101-A
  Booking 1: Rahul (Jan-Jun 2024) [EXITED]
  Booking 2: Amit (Jul-Dec 2024) [ACTIVE]
  Booking 3: Priya (Jan 2025 onwards) [Future booking]
  ```
- **Business Logic:** Enables bed occupancy history and future booking management

**Key Booking Fields Explained:**
- `start_date`: When tenant moved in
- `end_date`: When tenant moved out (NULL for active bookings)
- `status`: ACTIVE, NOTICE_PERIOD, EXITED, CANCELLED
- `rent_amount`: Monthly rent for this booking
- `deposit_amount`: Security deposit paid
- `is_zero_deposit`: Whether fintech partner provided deposit (USP 8)
- `notice_given_date`: When tenant gave notice to leave (USP 9)

### `DigitalAgreement` - E-Signed Contracts
**Purpose:** Stores digitally signed rental agreements (USP 7: Digital Agreement)

#### Relationships:

**1. `DigitalAgreement` ↔ `Booking` (booking) - 1:1 Relationship**
- **Field:** `booking = OneToOneField(Booking, primary_key=True)`
- **Meaning:** Each booking has exactly one rental agreement
- **Real Example:**
  ```
  Booking: Rahul in Room 101-A (ID: 12345)
  Agreement: rental_agreement_12345.pdf (signed: True, signed_at: Jan 1, 2024)
  ```
- **Business Logic:** Legal compliance and paperless documentation
- **Database Behavior:** If booking is deleted, agreement is also deleted (CASCADE)

---

## 4. 💸 `finance` App Relationships

### `Invoice` - Monthly Bills
**Purpose:** Generates monthly bills for tenants including rent, mess charges, electricity, etc.

#### Relationships:

**1. `Invoice` ↔ `Booking` (booking) - N:1 Relationship**
- **Field:** `booking = ForeignKey(Booking)`
- **Meaning:** Each booking can have multiple invoices (monthly bills)
- **Real Example:**
  ```
  Booking: Rahul in Room 101-A (6-month stay)
  Invoice 1: January 2024 (Rent: ₹8000, Mess: ₹3000, Electricity: ₹500)
  Invoice 2: February 2024 (Rent: ₹8000, Mess: ₹2800, Electricity: ₹600)
  Invoice 3: March 2024 (Rent: ₹8000, Mess: ₹3200, Electricity: ₹450)
  ```
- **Business Logic:** Automated monthly billing with itemized charges
- **Database Behavior:** PROTECT prevents booking deletion if unpaid invoices exist

**Invoice Components:**
- `rent_amount`: Base monthly rent
- `mess_charges`: Food charges from mess wallet usage
- `electricity_charges`: Individual bed consumption charges
- `late_fee`: Penalty for delayed payment
- `total_amount`: Sum of all charges
- `is_paid`: Payment status
- `due_date`: Payment deadline

### `Transaction` - Financial Movement Log
**Purpose:** Records all money movements in the system (payments, refunds, expenses, salaries)

#### Relationships:

**1. `Transaction` ↔ `CustomUser` (user) - N:1 Relationship**
- **Field:** `user = ForeignKey(CustomUser)`
- **Meaning:** Each transaction is associated with a user (who paid/received money)
- **Real Example:**
  ```
  User: Rahul (Tenant)
  Transaction 1: Rent Payment ₹8000 (Credit to PG)
  Transaction 2: Wallet Recharge ₹2000 (Credit to PG)
  Transaction 3: Security Refund ₹15000 (Debit from PG)
  ```

**2. `Transaction` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each transaction affects a specific property's finances
- **Business Logic:** Enables property-wise profit/loss calculation

**3. `Transaction` ↔ `Invoice` (invoice) - N:1 Relationship (Optional)**
- **Field:** `invoice = ForeignKey(Invoice, null=True, blank=True)`
- **Meaning:** Some transactions are linked to specific invoices (bill payments)
- **Real Example:**
  ```
  Invoice: January 2024 - ₹11500
  Transaction 1: ₹8000 (Partial payment)
  Transaction 2: ₹3500 (Remaining payment)
  ```

**Transaction Categories:**
- `RENT`: Monthly rent payments
- `WALLET_RECHARGE`: Mess wallet top-ups
- `MESS_DEBIT`: Daily meal deductions
- `REFUND`: Security deposit returns
- `EXPENSE`: Operational costs
- `SALARY`: Staff payments

### `Expense` - Operational Costs
**Purpose:** Tracks all business expenses for profit calculation (Advanced Feature 2: Expense Management)

#### Relationships:

**1. `Expense` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each expense is recorded against a specific property
- **Real Example:**
  ```
  Property: Gokuldham PG
  Expense 1: Groceries ₹15000 (Jan 2024)
  Expense 2: Electricity Bill ₹8000 (Jan 2024)
  Expense 3: WiFi Bill ₹2000 (Jan 2024)
  Expense 4: Plumber Service ₹1500 (Jan 2024)
  Total Monthly Expenses: ₹26500
  ```
- **Business Logic:** 
  ```
  Net Profit = Total Rent Collection - Total Expenses
  Example: ₹80000 (rent) - ₹26500 (expenses) = ₹53500 profit
  ```

---

## 5. 🛠️ `operations` App Relationships

### `Complaint` - Issue Management System
**Purpose:** Handles tenant complaints and maintenance requests with tracking and resolution

#### Relationships:

**1. `Complaint` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** One tenant can raise multiple complaints
- **Real Example:**
  ```
  Tenant: Rahul
  Complaint 1: "AC not working in Room 101" (Status: RESOLVED)
  Complaint 2: "WiFi slow in common area" (Status: IN_PROGRESS)
  Complaint 3: "Water leakage in bathroom" (Status: OPEN)
  ```

**2. `Complaint` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each complaint is specific to a property location
- **Business Logic:** Enables property-wise complaint tracking and manager assignment

**Complaint Workflow:**
1. Tenant raises complaint via app
2. Manager gets notification
3. Status changes: OPEN → IN_PROGRESS → RESOLVED
4. Tenant can rate the resolution (feedback system)

### `EntryLog` - Security & Safety Tracking
**Purpose:** Records all entry/exit activities for safety and parent monitoring (USP 12: Biometric/QR Entry)

#### Relationships:

**1. `EntryLog` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant has multiple entry/exit records
- **Real Example:**
  ```
  Tenant: Rahul
  Log 1: Entry at 08:30 AM (Method: QR_CODE)
  Log 2: Exit at 06:45 PM (Method: BIOMETRIC)
  Log 3: Entry at 11:30 PM (Method: MANUAL, is_late_entry: True)
  ```

**2. `EntryLog` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Tracks which property gate was used
- **Business Logic:** Multi-property tenants can access different locations

**Safety Features:**
- `is_late_entry`: Flags entries after 11 PM
- `parent_alert_sent`: Tracks if parent was notified of late entry
- `entry_method`: BIOMETRIC, QR_CODE, or MANUAL (by guard)

### `Notice` - Communication System
**Purpose:** Digital notice board for property-wide announcements (Advanced Feature 7)

#### Relationships:

**1. `Notice` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Each notice is specific to a property
- **Real Example:**
  ```
  Property: Gokuldham PG
  Notice 1: "Water supply will be off from 2-4 PM tomorrow"
  Notice 2: "New WiFi password: GokuldhamPG2024"
  Notice 3: "Diwali celebration on Oct 31st in common area"
  ```
- **Business Logic:** Push notifications sent to all tenants of that property

### `ChatLog` - AI Assistant Interactions
**Purpose:** Stores conversations between tenants and AI chatbot (USP 14: AI Chatbot)

#### Relationships:

**1. `ChatLog` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant has their own chat history with the bot
- **Real Example:**
  ```
  Tenant: Rahul
  Chat 1: "What's for lunch today?" → "Today's menu: Dal, Rice, Sabzi"
  Chat 2: "WiFi not working" → "I've logged a complaint for you. Ticket #1234"
  Chat 3: "When is rent due?" → "Your rent is due on 1st of every month"
  ```
- **Business Logic:** Enables 24/7 support and reduces manager workload

**AI Features:**
- `intent`: Categorizes query type (rent_query, complaint, menu_inquiry)
- `message`: User's question
- `bot_response`: AI's answer
- Integration with complaint system for automatic ticket creation

### `SOSAlert` - Emergency Response System
**Purpose:** Handles panic button alerts for tenant safety (USP 11: Women Safety & SOS Button)

#### Relationships:

**1. `SOSAlert` ↔ `CustomUser` (tenant) - N:1 Relationship**
- **Field:** `tenant = ForeignKey(CustomUser, limit_choices_to={'role': 'TENANT'})`
- **Meaning:** Each tenant can trigger multiple SOS alerts
- **Real Example:**
  ```
  Tenant: Priya
  Alert 1: Triggered at 11:45 PM (Status: RESOLVED, Response time: 3 minutes)
  Alert 2: Triggered at 02:30 AM (Status: FALSE_ALARM)
  ```

**2. `SOSAlert` ↔ `Property` (property) - N:1 Relationship**
- **Field:** `property = ForeignKey(Property)`
- **Meaning:** Alert is associated with property for jurisdiction and response

**3. `SOSAlert` ↔ `CustomUser` (first_responder) - N:1 Relationship**
- **Field:** `first_responder = ForeignKey(CustomUser, related_name='responded_sos_alerts')`
- **Meaning:** Tracks which staff member responded first
- **Business Logic:** Performance tracking and accountability

**Emergency Response Workflow:**
1. Tenant presses SOS button in app
2. GPS location captured automatically
3. Instant alerts sent to: Manager, Security, Parents, Owner
4. First responder acknowledges and responds
5. Incident resolution and classification (genuine/false alarm)

**Critical SOS Fields:**
- `latitude/longitude`: GPS coordinates for location
- `triggered_at`: Exact time of emergency
- `response_time_seconds`: How quickly help arrived
- `manager_notified/parent_notified`: Confirmation of alert delivery
- `is_genuine_emergency`: Post-incident classification

---

## 6. 🍛 `mess` App Relationships

### `MessMenu`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Weekly menu is defined per property.
    *   *Constraint:* Unique per Date + Property.

### `DailyMealSelection`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* The student making the meal choice.
*   **N -- 1** with `MessMenu` (`menu`)
    *   *Context:* The menu (Date) for which the choice is made.

---

## 7. 🤝 `crm` App Relationships

### `Lead`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* A lead (enquiry) is for a specific branch.
*   **1 -- 1** with `CustomUser` (`converted_tenant`)
    *   *Context:* (Optional) If the lead converts, links to their new User account.

---

## 8. 🔔 `notifications` App Relationships

### `NotificationLog`
*   **N -- 1** with `CustomUser` (`user`)
    *   *Context:* Log of SMS/Push notifications sent to a user.

### `FCMToken`
*   **N -- 1** with `CustomUser` (`user`)
    *   *Context:* Firebase device tokens belonging to a user.

---

## 9. 🛑 `visitors` App Relationships

### `VisitorRequest`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* The student whom the visitor wants to meet.
*   **N -- 1** with `Property` (`property`)
    *   *Context:* The property where the visit is happening.
*   **N -- 1** with `CustomUser` (`guard`)
    *   *Context:* The security guard who processed the entry.

---

## 10. 📦 `inventory` App Relationships

### `InventoryItem`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Stock items (Rice, Oil) belonging to a property's kitchen.

### `InventoryTransaction`
*   **N -- 1** with `InventoryItem` (`item`)
    *   *Context:* Movement (Purchase/Consumption) of a specific item.
*   **N -- 1** with `CustomUser` (`recorded_by`)
    *   *Context:* The staff member (Cook/Manager) who recorded the transaction.

---

## 11. 👷 `payroll` App Relationships

### `StaffAttendance`
*   **N -- 1** with `CustomUser` (`staff`)
    *   *Context:* Daily attendance record for a staff member.

### `SalaryPayment`
*   **N -- 1** with `CustomUser` (`staff`)
    *   *Context:* Monthly salary payment to a staff member.
*   **N -- 1** with `Property` (`property`)
    *   *Context:* The property account from which salary is paid.

---

## 12. 🧹 `hygiene` App Relationships

### `HygieneInspection`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Cleanliness audit for a property.
*   **N -- 1** with `CustomUser` (`inspector`)
    *   *Context:* The Manager/SuperAdmin who performed the audit.

---

## 13. ⭐ `feedback` App Relationships

### `ComplaintFeedback`
*   **1 -- 1** with `Complaint` (`complaint`)
    *   *Context:* Rating given for a specific resolved complaint.

### `MessFeedback`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* Student giving feedback on food.
*   **N -- 1** with `MessMenu` (`menu`)
    *   *Context:* The specific day's menu being rated.

---

## 14. 🕵️ `audit` App Relationships

### `AuditLog`
*   **N -- 1** with `CustomUser` (`user`)
    *   *Context:* The user who performed the action (Create/Update/Delete).

---



---

## 🏁 Summary of Key Hubs

### 1. **`CustomUser`** - The Authentication & Identity Hub
**Why It's Central:** Every action in the system is performed by a user

**Connected To:**
- **Profiles:** TenantProfile, StaffProfile (identity extension)
- **Properties:** Property ownership and management
- **Bookings:** Tenant stays and reservations
- **Finance:** Transactions, invoices, salary payments
- **Operations:** Complaints, entry logs, SOS alerts, chat logs
- **Feedback:** Complaint ratings, mess reviews
- **Visitors:** Visitor requests and approvals
- **Inventory:** Stock transaction records
- **Payroll:** Staff attendance and salary
- **Hygiene:** Inspection records
- **Notifications:** SMS, email, push notification logs
- **Audit:** Activity tracking for security


