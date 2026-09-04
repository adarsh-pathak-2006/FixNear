<div align="center">

# 🔧 FixNear

**A location-aware service-marketplace API that instantly connects customers with nearby skilled technicians.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.x-red?style=for-the-badge)](https://django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge&logo=jsonwebtokens)](https://jwt.io)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

</div>

---

## 📖 What is FixNear?

FixNear is a **Django REST API** backend for a two-sided service marketplace. A **customer** posts a repair request (e.g. *"my laptop won't turn on"*), and the platform **automatically finds and notifies every available technician** with the matching skill — in real time via Django signals. The technician can then accept or decline the job, and update the repair status as the work progresses.

> Think of it as an Uber-style matching system, but for repair professionals.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 **Role-based auth** | Separate `CUSTOMER` and `TECHNICIAN` roles with JWT access + refresh tokens |
| ⚡ **Auto-matching** | Django signals instantly dispatch a `SentRequest` to every available technician with the right skill when a job is posted |
| 🛡️ **Ownership enforcement** | Technicians can only accept, reject, or update *their own* requests |
| 📄 **Pagination** | All list endpoints paginate (10 per page, configurable) |
| 🚦 **Throttling** | Per-role, per-endpoint rate limits prevent abuse |
| 🗄️ **Caching** | Profile and list views are cached; signals invalidate stale keys automatically |
| 👤 **Auto-profiles** | A `CustomerProfile` or `TechnicianProfile` is auto-created on registration via signals |

---

## 🗺️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FixNear API                             │
│                                                                 │
│   ┌──────────────┐    POST /customer/repair-request/            │
│   │   Customer   │ ──────────────────────────────────────────►  │
│   └──────────────┘                                              │
│                              ▼                                  │
│                    RepairRequest created                        │
│                              │                                  │
│                    post_save signal fires                       │
│                              │                                  │
│                              ▼                                  │
│              Filter: TechnicianProfile WHERE                    │
│              skill = skills_required AND is_available = True    │
│                              │                                  │
│              ┌───────────────┼───────────────┐                 │
│              ▼               ▼               ▼                 │
│         SentRequest     SentRequest     SentRequest            │
│         (Tech A)        (Tech B)        (Tech C)               │
│              │               │               │                 │
│   ┌──────────┘               └───────────────┘                 │
│   │                                                             │
│   │   GET /technician/all-request/                             │
│   ▼                                                             │
│   ┌───────────────┐                                             │
│   │  Technician   │  PATCH /technician/request/<id>/           │
│   └───────────────┘  (accept = True → Repair row created)      │
│                                                                 │
│              PATCH /technician/status/<id>/                     │
│              PENDING → PROCESSING → COMPLETED                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
fixnear/
├── fixnear/                  ← Django project package
│   ├── settings.py           ← Configuration (reads from .env)
│   ├── urls.py               ← Root URL router
│   ├── apps.py               ← Connects signals on startup
│   ├── signals.py            ← Auto-profile creation & matching logic
│   ├── permissions.py        ← IsCustomer / IsTechnician / both
│   ├── throttling.py         ← Per-endpoint rate limits
│   ├── pagination.py         ← Shared 10-per-page paginator
│   ├── cache_key.py          ← Centralised cache key helpers
│   └── constants.py          ← Shared SKILL_CHOICES
│
├── authentication/           ← Users & profiles
│   ├── models.py             ← User, CustomerProfile, TechnicianProfile
│   ├── serializers.py
│   ├── views.py              ← Register, login, profile CRUD, technician list
│   └── urls.py
│
├── customer/                 ← Repair request submission
│   ├── models.py             ← RepairRequest
│   ├── serializers.py
│   ├── views.py              ← POST a repair request
│   └── urls.py
│
├── technician/               ← Job management
│   ├── models.py             ← SentRequest, Repair
│   ├── serializers.py
│   ├── views.py              ← List jobs, accept/decline, update status
│   └── urls.py
│
├── .env                      ← Secret config (never committed)
├── .env.example              ← Template for contributors
├── requirements.txt
└── manage.py
```

---

## 🔗 API Reference

### Authentication — `/auth/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register/` | ❌ | Register a new user (customer or technician) |
| `POST` | `/auth/token/` | ❌ | Login — returns `access` + `refresh` JWT tokens |
| `POST` | `/auth/token/refresh/` | ❌ | Refresh an expired access token |
| `GET` | `/auth/my-profile/` | Customer | View your customer profile |
| `PATCH` | `/auth/my-profile/` | Customer | Update location, etc. |
| `GET` | `/auth/my-technician-profile/` | Technician | View your technician profile |
| `PATCH` | `/auth/my-technician-profile/` | Technician | Update bio, skill, availability |
| `GET` | `/auth/technicians/` | Both | Browse available technicians (paginated) |

### Customer — `/customer/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/customer/repair-request/` | Customer | Submit a new repair job request |

### Technician — `/technician/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/technician/all-request/` | Technician | List all repair requests assigned to you (paginated) |
| `PATCH` | `/technician/request/<id>/` | Technician | Accept a request (`is_accepted: true`) |
| `DELETE` | `/technician/request/<id>/` | Technician | Decline / remove a request |
| `PATCH` | `/technician/status/<id>/` | Technician | Update repair status (`PENDING` → `PROCESSING` → `COMPLETED`) |

---

## 🔄 Request Lifecycle

```
Customer POSTs /customer/repair-request/
        │
        ▼
  RepairRequest saved in DB
        │
        ▼  (post_save signal)
  Find all TechnicianProfiles WHERE
  skill = skills_required AND is_available = True
        │
        ▼  (bulk_create)
  SentRequest created for each matching technician
        │
        ▼  (post_save signal)
  Cache invalidated for each technician's request list
        │
        ▼
  Technician GETs /technician/all-request/
  Technician PATCHes /technician/request/<id>/ with { "is_accepted": true }
        │
        ▼
  Repair object created (status = PENDING)
        │
        ▼
  Technician PATCHes /technician/status/<id>/ to update progress
```

---

## 🛠️ Skills & Roles

### Available Skills

| Skill Key | Label |
|---|---|
| `MOBILE_REPAIR` | Mobile Repair |
| `LAPTOP_REPAIR` | Laptop Repair |
| `PLUMBER` | Plumber |
| `ELECTRICIAN` | Electrician |

### User Roles

| Role | Can do |
|---|---|
| `CUSTOMER` | Post repair requests, browse technicians, manage own profile |
| `TECHNICIAN` | View assigned jobs, accept/decline, update repair status |
| `ADMIN` | Full Django admin panel access |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip

### 1 — Clone & set up virtual environment

```bash
git clone https://github.com/your-username/fixnear.git
cd fixnear
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### 3 — Configure environment

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
SECRET_KEY=your-very-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> 💡 Generate a secure secret key with:
> ```bash
> python -c "from django.core.signing import get_cookie_signer; print(get_cookie_signer().key)"
> ```

### 4 — Run migrations

```bash
python manage.py migrate
```

### 5 — Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6 — Start the development server

```bash
python manage.py runserver
```

API is now live at **`http://127.0.0.1:8000/`**

---

## 📬 Example Requests

### Register a customer

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "mobile_no": "9876543210",
    "role": "CUSTOMER",
    "password": "strongpassword123"
  }'
```

### Get a JWT token

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "strongpassword123"}'
```

### Post a repair request (as customer)

```bash
curl -X POST http://127.0.0.1:8000/customer/repair-request/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "skills_required": "LAPTOP_REPAIR",
    "requirement": "My laptop screen is cracked and won'\''t display anything."
  }'
```

### Accept a job (as technician)

```bash
curl -X PATCH http://127.0.0.1:8000/technician/request/3/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"is_accepted": true}'
```

---

## ⚙️ Configuration Reference

All settings are loaded from `.env` via `python-decouple`.

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | — | Django secret key (**required**) |
| `DEBUG` | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated list of allowed hosts |

### Rate Limits

| Throttle | Class | Limit |
|---|---|---|
| Registration | `AnonRateThrottle` (IP-based) | 20 / hour |
| Token obtain (login) | `AnonRateThrottle` (IP-based) | 30 / hour |
| Token refresh | `UserRateThrottle` | 7 / hour |
| All other endpoints | `UserRateThrottle` | 30 / minute |

### JWT Token Lifetimes

| Token | Lifetime |
|---|---|
| Access token | 30 minutes |
| Refresh token | 7 days |

---

## 🏗️ Data Models

```
User (AbstractUser)
├── mobile_no   CharField
└── role        CharField  [CUSTOMER | TECHNICIAN | ADMIN]

CustomerProfile  ──────────────── OneToOne ──► User
├── latitude     CharField
├── longitude    CharField
├── is_verified  BooleanField
└── created_on   DateTimeField

TechnicianProfile ─────────────── OneToOne ──► User
├── bio           TextField
├── experience    PositiveIntegerField
├── average_rating DecimalField
├── total_job     PositiveIntegerField
├── skill         CharField  [MOBILE_REPAIR | LAPTOP_REPAIR | PLUMBER | ELECTRICIAN]
├── is_available  BooleanField
└── created_on    DateTimeField

RepairRequest ─────────────────── ForeignKey ──► CustomerProfile
├── skills_required  CharField
├── requirement      TextField
└── created_on       DateTimeField

SentRequest ───────────────────── ForeignKey ──► TechnicianProfile
│           ───────────────────── ForeignKey ──► RepairRequest
├── is_accepted  BooleanField
└── created_on   DateTimeField

Repair ─────────────────────────── OneToOne ──► SentRequest
├── status      CharField  [PENDING | PROCESSING | COMPLETED]
└── updated_on  DateTimeField
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

<div align="center">
Made with ❤️ · FixNear
</div>
