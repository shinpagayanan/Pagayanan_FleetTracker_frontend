# 🚗 Fleet Maintenance Tracker — Frontend

A server-rendered web frontend for the Fleet Maintenance Tracker system. Built with Django templates, it communicates with the [Fleet Maintenance Tracker Backend](https://github.com/) via REST API and provides role-specific dashboards and interfaces for Managers, Auditors, and Staff.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Template Structure](#template-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Development Server](#running-the-development-server)
- [Pages & Features](#pages--features)
- [Deployment](#deployment)

---

## 📌 Overview

This frontend serves as the user-facing layer of the Fleet Maintenance Tracker. It renders role-based views by consuming data from the backend REST API and enforces access control at the template level — each role (Manager, Auditor, Staff) gets its own base layout and dashboard.

---

## 🗂 Template Structure

```
templates/
├── assets/
│   ├── asset_detail.html        # View a single asset's details
│   ├── assets_list.html         # Manager/Auditor: full asset listing
│   ├── assign_asset.html        # Assign an asset to a staff member
│   ├── bulk_assign.html         # Bulk-assign multiple assets
│   ├── create_asset.html        # Create a new asset
│   ├── edit_asset.html          # Edit an existing asset
│   └── staff_assets_list.html   # Staff: view only assigned assets
│
├── audit_logs/
│   └── audit_log_list.html      # Full audit trail (Manager & Auditor)
│
├── auth/
│   └── login.html               # JWT login page
│
├── dashboard/
│   ├── dashboard_base.html      # Shared dashboard base layout
│   ├── dashboard.html           # Default dashboard redirect
│   ├── manager_base.html        # Manager base layout
│   ├── manager_dashboard.html   # Manager dashboard view
│   ├── auditor_base.html        # Auditor base layout
│   ├── auditor_dashboard.html   # Auditor dashboard view
│   ├── staff_base.html          # Staff base layout
│   └── staff_dashboard.html     # Staff dashboard view
│
├── mileage/
│   ├── history.html             # View mileage log history
│   └── submit.html              # Submit a new mileage entry
│
├── reports/
│   ├── asset_report.html        # Asset summary report
│   ├── maintenance_report.html  # Maintenance request report
│   ├── mileage_report.html      # Mileage report
│   └── workorder_report.html    # Work order report
│
├── requests/
│   ├── create_request.html      # Staff: submit a maintenance request
│   ├── manager_requests.html    # Manager: view & approve/reject requests
│   └── my_requests.html         # Staff: view own submitted requests
│
├── users/
│   ├── create_user.html         # Create a new user (Manager only)
│   ├── delete_user.html         # Delete a user (Manager only)
│   ├── edit_user.html           # Edit a user (Manager only)
│   └── user_list.html           # List all users (Manager only)
│
└── workorders/
    ├── detail.html              # View a single work order
    └── list.html                # List all work orders
```

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12+ |
| Framework | Django |
| Templating | Django Templates (Jinja-compatible) |
| Styling | HTML/CSS |
| API Communication | Backend REST API (via `BACKEND_API_URL`) |
| Deployment | Render |

---

## ✅ Prerequisites

- Python 3.12 or higher
- Git

Verify your installation:

```bash
python --version
pip --version
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <frontend-repository-url>
cd fleettracker-frontend
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=False
BACKEND_API_URL=https://pagayanan-fleettracker-backend.onrender.com/api
```

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key for session and CSRF security |
| `DEBUG` | Enable or disable debug mode (`True` for local dev) |
| `BACKEND_API_URL` | Base URL of the Fleet Maintenance Tracker backend API |

> ⚠️ Never commit your `.env` file to version control. Add it to `.gitignore`.

---

## ▶️ Running the Development Server

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`

> Make sure the backend API is running and reachable at the URL set in `BACKEND_API_URL`.

---

## 📄 Pages & Features

### 🔑 Authentication
- Login page with JWT token handling
- Automatic role detection and dashboard redirect on login

### 📊 Dashboards
Each role gets a dedicated dashboard with relevant statistics and quick-access links:

| Role | Dashboard |
|------|-----------|
| Manager | System-wide stats, pending requests, work order overview |
| Auditor | Read-only stats, audit log access, report links |
| Staff | Assigned assets, submitted requests, mileage log |

### 🏷 Assets
- Full asset listing (Manager/Auditor)
- Asset detail view
- Create, edit, and delete assets (Manager)
- Assign assets to staff — individually or in bulk (Manager)
- Staff view of assigned assets only

### 🔧 Maintenance Requests
- Staff can submit new requests and track their own
- Manager can view all requests and approve or reject them

### 📋 Work Orders
- Auto-generated on request approval
- List and detail views for all roles
- Manager can mark work orders as complete

### 📏 Mileage Logs
- Staff can submit mileage entries for vehicles
- Full mileage history view

### 📈 Reports *(Manager & Auditor)*
- Asset summary report
- Maintenance request report
- Work order report
- Mileage report

### 🕵️ Audit Logs *(Manager & Auditor)*
- Full chronological trail of all system actions

### 👤 User Management *(Manager only)*
- List, create, edit, and delete users

---

## ☁️ Deployment

The frontend is deployed on **Render**.

### Steps

1. Push repository to GitHub
2. Create a Render Web Service
3. Configure environment variables (`SECRET_KEY`, `DEBUG`, `BACKEND_API_URL`)
4. Deploy the application

Collect static files before deploying:

```bash
python manage.py collectstatic --noinput
```
