# Django Table Reservation System Documentation

A comprehensive Django web application for managing restaurant table reservations, customer details, seating categories, payments, and audit logs.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Database Architecture & Models](#database-architecture--models)
3. [Forms & Validation Rules](#forms--validation-rules)
4. [API Views & Features](#api-views--features)
5. [URL Endpoints Reference](#url-endpoints-reference)
6. [Django Admin Interface](#django-admin-interface)
7. [Installation & Setup Guide](#installation--setup-guide)
8. [System Verification](#system-verification)

---

## Project Overview

The **Django Table Reservation System** (`reservation_app`) is designed to handle online and in-house table bookings for restaurants. It tracks:
- Customer records and contact details
- Restaurant table categories and table capacities
- Reservation scheduling with built-in validation rules
- Payment tracking for reservations
- Automatic audit logging for tracking system and user actions

---

## Database Architecture & Models

The database consists of **7 relational models**:

### 1. `Customer`
Stores customer profile information.
- `id` (AutoField / BigAutoField): Primary key
- `first_name` (CharField, max length 100): Customer's first name
- `last_name` (CharField, max length 100): Customer's last name
- `email` (EmailField, unique): Unique email address
- `phone` (CharField, max length 20, unique): Unique telephone number
- `created_at` (DateTimeField): Auto timestamp on creation
- `updated_at` (DateTimeField): Auto timestamp on update

### 2. `TableCategory`
Categorizes tables (e.g., Main Dining, Patio, VIP Room).
- `id` (AutoField / BigAutoField): Primary key
- `name` (CharField, max length 100, unique): Category title
- `description` (TextField, optional): Category details
- `created_at`, `updated_at`: Timestamps

### 3. `Table`
Represents individual reservable restaurant tables.
- `id` (AutoField / BigAutoField): Primary key
- `table_number` (CharField, max length 20, unique): Identifier (e.g., T01, T02)
- `category` (ForeignKey $\rightarrow$ `TableCategory`): Assigned category
- `capacity` (PositiveIntegerField): Maximum guest capacity
- `location` (CharField, max length 100): Physical location description
- `is_active` (BooleanField, default True): Active table flag
- `created_at`, `updated_at`: Timestamps

### 4. `ReservationStatus`
Standardized status options for reservations (e.g., PENDING, CONFIRMED, CANCELLED).
- `id` (AutoField / BigAutoField): Primary key
- `name` (CharField, max length 50, unique): Status name
- `description` (TextField, optional): Description
- `is_active` (BooleanField, default True): Status availability flag
- `created_at`, `updated_at`: Timestamps

### 5. `Reservation`
Core entity connecting customers, tables, and statuses.
- `id` (AutoField / BigAutoField): Primary key
- `customer` (ForeignKey $\rightarrow$ `Customer`): Booking customer
- `table` (ForeignKey $\rightarrow$ `Table`): Booked table
- `reservation_date` (DateField): Date of reservation
- `start_time` (TimeField): Start time
- `end_time` (TimeField): End time
- `guests` (PositiveIntegerField): Number of guests
- `status` (ForeignKey $\rightarrow$ `ReservationStatus`): Current status
- `notes` (TextField, optional): Special instructions
- `created_at`, `updated_at`: Timestamps

### 6. `Payment`
Tracks payments associated with reservations.
- `id` (AutoField / BigAutoField): Primary key
- `reservation` (ForeignKey $\rightarrow$ `Reservation`): Linked reservation
- `amount` (DecimalField, max_digits=10, decimal_places=2): Amount paid/due
- `payment_method` (CharField, max length 50): Method (e.g., Credit Card, Cash)
- `payment_status` (CharField, choices: `PENDING`, `PAID`, `FAILED`, `REFUNDED`)
- `paid_at` (DateTimeField, optional): Payment completion timestamp
- `transaction_id` (CharField, unique, optional): External transaction reference
- `created_at`, `updated_at`: Timestamps

### 7. `AuditLog`
Audit trailing for key events on reservations.
- `id` (AutoField / BigAutoField): Primary key
- `reservation` (ForeignKey $\rightarrow$ `Reservation`): Linked reservation
- `action` (CharField, max length 100): Action code (`CREATE`, `UPDATE`, `CANCEL`)
- `performed_by` (CharField, max length 100): User or system trigger
- `action_time` (DateTimeField): Event timestamp
- `details` (TextField, optional): Log details

---

## Forms & Validation Rules

All models use Django `ModelForm` wrappers located in `reservation_app/forms.py`.

### Key Validation Logic:
1. **Positive Guest Count:**
   - Enforces `guests > 0`.
2. **Reservation Time Validation:**
   - Enforces `end_time > start_time`.
3. **Table Capacity Check:**
   - Verifies that `guests <= table.capacity`. If violated, raises a `ValidationError` specifying table capacity.

---

## API Views & Features

Defined in `reservation_app/views.py`:
- **JSON REST endpoints:** Returns clean JSON payloads for all List, Detail, Create, Update, and Delete operations.
- **Automatic Audit Generation:** Creating, updating, or cancelling reservations automatically records an entry into `AuditLog`.
- **Query Parameter Filtering:**
  - `GET /reservations/?customer=<id>`: Filter by customer
  - `GET /reservations/?date=YYYY-MM-DD`: Filter by date
  - `GET /payments/?reservation=<id>`: Filter payments by reservation
  - `GET /audit-logs/?reservation=<id>`: Filter logs by reservation

---

## URL Endpoints Reference

Base app namespace: `reservation_app`

| Model | Verb | Endpoint Path | URL Name |
| :--- | :--- | :--- | :--- |
| **Customer** | GET | `/customers/` | `customer_list` |
| | POST | `/customers/add/` | `customer_create` |
| | GET | `/customers/<pk>/` | `customer_detail` |
| | POST/PUT | `/customers/<pk>/edit/` | `customer_update` |
| | POST/DELETE | `/customers/<pk>/delete/` | `customer_delete` |
| **Table Category** | GET | `/table-categories/` | `table_category_list` |
| | POST | `/table-categories/add/` | `table_category_create` |
| | GET | `/table-categories/<pk>/` | `table_category_detail` |
| | POST/PUT | `/table-categories/<pk>/edit/` | `table_category_update` |
| | POST/DELETE | `/table-categories/<pk>/delete/` | `table_category_delete` |
| **Table** | GET | `/tables/` | `table_list` |
| | POST | `/tables/add/` | `table_create` |
| | GET | `/tables/<pk>/` | `table_detail` |
| | POST/PUT | `/tables/<pk>/edit/` | `table_update` |
| | POST/DELETE | `/tables/<pk>/delete/` | `table_delete` |
| **Reservation Status** | GET | `/reservation-statuses/` | `reservation_status_list` |
| | POST | `/reservation-statuses/add/` | `reservation_status_create` |
| | POST/PUT | `/reservation-statuses/<pk>/edit/` | `reservation_status_update` |
| | POST/DELETE | `/reservation-statuses/<pk>/delete/` | `reservation_status_delete` |
| **Reservation** | GET | `/reservations/` | `reservation_list` |
| | POST | `/reservations/add/` | `reservation_create` |
| | GET | `/reservations/<pk>/` | `reservation_detail` |
| | POST/PUT | `/reservations/<pk>/edit/` | `reservation_update` |
| | POST | `/reservations/<pk>/cancel/` | `reservation_cancel` |
| **Payment** | GET | `/payments/` | `payment_list` |
| | POST | `/payments/add/` | `payment_create` |
| | GET | `/payments/<pk>/` | `payment_detail` |
| | POST/PUT | `/payments/<pk>/edit/` | `payment_update` |
| **Audit Log** | GET | `/audit-logs/` | `audit_log_list` |
| | GET | `/audit-logs/<pk>/` | `audit_log_detail` |

---

## Django Admin Interface

All 7 models are registered in `reservation_app/admin.py`:
- `Customer`
- `TableCategory`
- `Table`
- `ReservationStatus`
- `Reservation`
- `Payment`
- `AuditLog`

---

## Installation & Setup Guide

### 1. Prerequisites
- Python 3.x installed
- Virtual environment created and activated

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

---

## System Verification

To run Django system checks:
```bash
python manage.py check
```
Result: **System check identified no issues (0 silenced).**
