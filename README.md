<<<<<<< HEAD
# CareerPulse — Aesthetic Job Application Tracker

An aesthetic, full-stack **Job Application Tracker** built with **Python 3.14**, **Django 6.1**, **SQL (SQLite)**, **HTML5**, **Vanilla CSS & Design System**, and **Bootstrap 5**.

Designed specifically as a showcase portfolio and resume project that demonstrates end-to-end web engineering, clean database modeling, dynamic CRUD workflows, responsive glassmorphic UI, and real-time candidate pipeline management.

---

## 📌 Resume Project Description

> **Job Tracker Application**  
> *Developed a web application to help users manage and track job applications. Implemented functionality to add, update, view, and organize job application records. Used Django models and SQL databases to store and manage application data. Created user-friendly web pages using HTML, CSS, and Bootstrap. Applied CRUD operations and backend logic to manage application status and details.*

---

## ✨ Key Features & Architecture

### 1. Aesthetic Modern Design System (Glassmorphism & Cyber/Aurora)
- **Theme Switcher**: Instant Dark Mode and Light Mode toggle with `localStorage` persistence.
- **Glassmorphic Cards**: `backdrop-filter: blur(12px)`, translucent card surfaces, glowing accent borders, and micro-hover animations.
- **Live Interview Radar**: Animated glowing radar pulse indicator on active interview opportunities.
- **Responsive Layout**: Designed for seamless experience on mobile, tablet, and desktop viewports.

### 2. Comprehensive CRUD & Pipeline Management
- **Add / Quick-Track**: Modal quick-add from any page (`Ctrl+K` or press `N`), plus a dedicated comprehensive application creation form.
- **View & Filter**:
  - Live search across company name, role, tags, location, and recruiter.
  - Multi-criteria filtering by Status (Wishlist, Applied, Interviewing, Offered, Rejected, Accepted, Withdrawn), Workplace Type (Remote, Hybrid, On-site), and Priority (High, Medium, Low).
  - View switcher: Toggle between **Table View** and **Card Grid View**.
- **Update**: In-place 1-click status dropdown updates (via AJAX) without page refresh, plus full dossier edit page.
- **Delete**: Safe delete dialog with confirmation to prevent accidental loss.
- **Interactive Kanban Board**: 5-column drag-and-drop workflow pipeline (*Wishlist*, *Applied*, *Interviewing*, *Offered*, *Rejected*) with count badges and fallback quick-move dropdowns.

### 3. Application Dossier & Timeline Milestones
- **Deep-dive Application View**: Company logo initials badge, job URL link, compensation, recruiter contact card (email & LinkedIn), job description, and personal preparation notes.
- **Stage Timeline**: Interactive stem timeline tracking each milestone (e.g., *Application Submitted*, *Recruiter Screen*, *Coding Assessment*, *Virtual Onsite*, *Offer Received*).

### 4. Quantitative Analytics & Insights
- Interactive **Chart.js** data visualizations:
  - Application Status Funnel (Doughnut chart)
  - Workplace Distribution (Remote vs Hybrid vs On-site bar chart)
  - Applications by Priority breakdown
  - Skill & Tech Stack frequency tags
  - Funnel health tips and response rate calculations.

### 5. Data Portability & Demo Seeder
- **CSV Data Export**: 1-click export of your complete application history into a formatted CSV spreadsheet.
- **One-Click Demo Seeder**: Integrated demo data generator (`python manage.py seed_data` or web button) that populates realistic sample applications (*Google*, *Stripe*, *Spotify*, *Airbnb*, *Amazon AWS*, etc.) with timeline stages for portfolio presentations.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.14, Django 6.1 (MTV Architecture) |
| **Database** | SQL / SQLite3 (Django ORM with migrations) |
| **Frontend UI** | HTML5, CSS3 Custom Design System, Bootstrap 5.3, Bootstrap Icons |
| **Data Visualizations** | Chart.js 4.4 |
| **Client Scripting** | Vanilla JavaScript (ES6+), HTML5 Drag & Drop API, Fetch API |
| **Testing** | Django `TestCase` test suite (13 automated unit tests) |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Python 3.14 supported)
- Django 5.0+ (`pip install -r requirements.txt`)

### 2. Setup & Database Migration
```bash
# Clone or navigate to the repository
cd Job_Application_Tracker

# Run database migrations
python manage.py migrate

# (Optional) Seed realistic sample jobs for portfolio demo
python manage.py seed_data
```

### 3. Launch Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your web browser.

---

## 🧪 Running Automated Tests
Run the Django test suite to verify all models, views, CRUD operations, AJAX endpoints, and CSV exports:
```bash
python manage.py test
```

---

## 📁 Project Directory Structure

```
Job_Application_Tracker/
├── job_tracker/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # App settings, templates, static & media setup
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── tracker/                     # Core tracker application
│   ├── migrations/              # Database migration schemas
│   ├── management/commands/     # CLI commands (e.g. seed_data.py)
│   ├── admin.py                 # Django admin registration
│   ├── forms.py                 # ModelForms for Applications & Timeline
│   ├── models.py                # JobApplication & ApplicationTimeline models
│   ├── tests.py                 # 13 automated unit tests
│   ├── urls.py                  # Tracker route definitions
│   └── views.py                 # View controllers & business logic
├── templates/                   # HTML Templates
│   ├── base.html                # Base layout, navbar, modals, theme switcher
│   └── tracker/
│       ├── dashboard.html       # Dashboard with KPIs, search, table/grid
│       ├── kanban.html          # Drag-and-drop pipeline board
│       ├── analytics.html       # Visual charts & conversion metrics
│       ├── application_detail.html # Dossier & timeline milestones
│       ├── application_form.html   # Add/Edit form
│       └── application_confirm_delete.html # Confirmation dialog
├── static/                      # Static assets
│   ├── css/custom.css           # Glassmorphic dark/light theme design system
│   └── js/main.js               # Theme toggle, drag-drop, AJAX status handler
├── requirements.txt             # Project dependencies
├── manage.py
└── README.md
```

---

## 💡 Interview Talking Points for Your Resume

When discussing this project in technical interviews, you can highlight:
1. **Django ORM & Model Design**: How `JobApplication` and `ApplicationTimeline` use relational foreign keys with cascade deletions, custom model properties (`days_since_applied`, `tag_list`), and efficient database querying using `Q` filters and aggregates.
2. **Dynamic Client-Server Interaction**: How AJAX status updates enable instant Kanban moves and table dropdown updates with JSON responses and optimistic UI updates without full page reloads.
3. **Responsive UI/UX**: Crafting a custom aesthetic design system with CSS custom properties (variables), glassmorphic styling, and accessible keyboard shortcuts.
4. **Data Portability**: Implementing a dynamic CSV streaming response with Django `HttpResponse` and Python's `csv` module.
=======
# job_application_tracker-
>>>>>>> origin/main
