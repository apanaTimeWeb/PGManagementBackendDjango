# 🔗 Database Tables Relationships & Associations

This document provides a **complete and exhaustive** guide to how database tables (models) are connected in the **Smart PG Management System**. It covers every single relationship defined in the codebase, ensuring new developers have 100% clarity on the data architecture.

---

## 🏗️ Legend & Concepts

*   **One-to-One (1:1):** One record in Table A is linked to exactly one record in Table B.
    *   *Symbol:* `1 -- 1`
*   **One-to-Many (1:N):** One record in Table A is linked to multiple records in Table B.
    *   *Symbol:* `1 -- N`
*   **Many-to-Many (M:N):** Multiple records in Table A are linked to multiple records in Table B.
    *   *Symbol:* `N -- N`

---

## 1. 👤 `users` App Relationships

### `CustomUser`
The central hub of the system.
*   **Note:** Referenced by almost every other table. See specific tables below for the connections.

### `TenantProfile`
*   **1 -- 1** with `CustomUser` (`user`)
    *   *Context:* Connects a user login to tenant-specific data (Credit score, Aadhaar).
*   **N -- 1** with `CustomUser` (`guardian`)
    *   *Context:* A tenant is linked to a Parent/Guardian user.
    *   *Example:* "Rahul" (Tenant) is the ward of "Mr. Sharma" (Parent).

### `StaffProfile`
*   **1 -- 1** with `CustomUser` (`user`)
    *   *Context:* Connects a user to staff details (Salary, Role).
*   **N -- 1** with `Property` (`assigned_property`)
    *   *Context:* A staff member works at a specific branch.
    *   *Example:* "Ramu" (Cook) works at "Gokuldham PG".

---

## 2. 🏨 `properties` App Relationships

### `Property`
*   **N -- 1** with `CustomUser` (`owner`)
    *   *Context:* A PG branch belongs to a SuperAdmin owner.
*   **N -- 1** with `CustomUser` (`manager`)
    *   *Context:* A PG branch is assigned a Manager.

### `Room`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Rooms exist within a property.

### `PricingRule`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Seasonal pricing rules apply to a specific property.

### `Bed`
*   **N -- 1** with `Room` (`room`)
    *   *Context:* Beds exist within a room.

### `ElectricityReading`
*   **N -- 1** with `Bed` (`bed`)
    *   *Context:* Meter readings are linked to a specific bed's IoT meter.

### `Asset`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Assets (AC, Geyser) belong to a property's inventory.
*   **N -- 1** with `Room` (`room`)
    *   *Context:* (Optional) An asset is installed in a specific room.

### `AssetServiceLog`
*   **N -- 1** with `Asset` (`asset`)
    *   *Context:* Service history records for a specific asset.

---

## 3. 📅 `bookings` App Relationships

### `Booking`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* A booking maps a student to their stay.
*   **N -- 1** with `Bed` (`bed`)
    *   *Context:* A booking reserves a specific bed.

### `DigitalAgreement`
*   **1 -- 1** with `Booking` (`booking`)
    *   *Context:* A rental agreement is generated for a specific booking.

---

## 4. 💸 `finance` App Relationships

### `Invoice`
*   **N -- 1** with `Booking` (`booking`)
    *   *Context:* Invoices are generated for a booking (Rent + Mess).

### `Transaction`
*   **N -- 1** with `CustomUser` (`user`)
    *   *Context:* The user who initiated the transaction (Tenant paying rent or Owner paying expense).
*   **N -- 1** with `Property` (`property`)
    *   *Context:* The property associated with the funds.
*   **N -- 1** with `Invoice` (`invoice`)
    *   *Context:* (Optional) Links a payment to a specific invoice.

### `Expense`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Operational expenses (Vegetables, Electricity) recorded for a branch.

---

## 5. 🛠️ `operations` App Relationships

### `Complaint`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* The student who raised the complaint.
*   **N -- 1** with `Property` (`property`)
    *   *Context:* The property where the issue occurred.

### `EntryLog`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* Biometric/QR entry record for a student.
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Which property gate they entered/exited.

### `Notice`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Digital notices are published for a specific branch.

### `ChatLog`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* Chat history between a tenant and the AI Bot.

### `SOSAlert`
*   **N -- 1** with `CustomUser` (`tenant`)
    *   *Context:* The student in distress who pressed the panic button.
*   **N -- 1** with `Property` (`property`)
    *   *Context:* The property jurisdiction for the alert.
*   **N -- 1** with `CustomUser` (`first_responder`)
    *   *Context:* The staff member who responded/acknowledged the alert.

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

## 15. 🎓 `alumni` App Relationships

### `AlumniProfile`
*   **1 -- 1** with `CustomUser` (`user`)
    *   *Context:* Extension of user profile for alumni.
*   **N -- N** with `Property` (`properties_stayed`)
    *   *Context:* List of all properties the alumni stayed in during their time.

### `JobReferral`
*   **N -- 1** with `CustomUser` (`requester`)
    *   *Context:* Current student asking for a referral.
*   **N -- 1** with `CustomUser` (`alumni`)
    *   *Context:* Ex-student (Alumni) receiving the request.

---

## 16. 💼 `saas` App Relationships

### `PropertySubscription`
*   **N -- 1** with `CustomUser` (`owner`)
    *   *Context:* The business owner subscribing to the software.
*   **N -- 1** with `SubscriptionPlan` (`plan`)
    *   *Context:* The SaaS plan (Gold/Platinum) linked to the subscription.

---

## 17. 📊 `reports` App Relationships

### `GeneratedReport`
*   **N -- 1** with `Property` (`property`)
    *   *Context:* Report generated for a specific branch context.
*   **N -- 1** with `CustomUser` (`generated_by`)
    *   *Context:* The user (Admin/Manager) who requested the report.

---

## 18. 🌍 `localization` App Relationships

### `TranslationString`
*   **N -- 1** with `CustomUser` (`updated_by`)
    *   *Context:* Admin who last updated the translation.

---

## 🏁 Summary of Key Hubs

1.  **`CustomUser`**: The most connected table. Linked to Profiles, Bookings, Properties, Complaints, Logs, Payments, etc.
2.  **`Property`**: The physical hub. Linked to Rooms, Expenses, Staff, Inspections, Notices, Lead, Visitors.
3.  **`Booking`**: The transactional hub. Links Users to Beds and is the parent for Invoices and Agreements.
