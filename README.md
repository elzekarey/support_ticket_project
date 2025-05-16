# 🎟️ Support ticket system

A concurrent-safe ticket assignment system built with Django & Django REST Framework. It ensures that no support agent gets more than 15 tickets and handles concurrent ticket fetching gracefully.

## 🚀 Features

- Token-based authentication with JWT
- Admin can create tickets
- Agents can fetch up to 15 tickets
- Agents cannot fetch more once 15 are assigned
- Only agents can fetch/sell tickets
- Concurrency-safe assignment logic
- Fully covered by unit and concurrency tests

---

## 📦 Tech Stack

- **Backend:** Django , Django REST Framework
- **Auth:** djangorestframework-simplejwt
- **Database:** PostgreSQL
- **Testing:** Django TransactionTestCase
- **Concurrency:** Python `threading` module

---

## 📂 Project Structure

```
Ticket/
├── tickets/           # Main app
│   ├── models.py      # User, Ticket models
│   ├── views.py       # API views
│   ├── admin.py       # Admin
│   ├── apps.py       # Apps
│   ├── permissions.py       # Permision checks
│   ├── serializers.py       # Serializers
│   ├── urls.py        # Routes for API
│   └── tests.py       # Unit + concurrency tests
├── ticket_project/            # Project settings
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/elzekarey/support_ticket_project.git
cd support_ticket_project
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL (recommended)

```sql
-- In PostgreSQL shell:
CREATE DATABASE ticket_db;
CREATE USER ticket_user WITH PASSWORD 'ticket_pass';
GRANT ALL PRIVILEGES ON DATABASE ticket_db TO ticket_user;
ALTER USER ticket_user CREATEDB;
```

Update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ticket_db',
        'USER': 'ticket_user',
        'PASSWORD': 'ticket_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🛠️ Running the Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🔑 Authentication

This project uses JWT:

- Obtain token: `POST /api/token/`
- Use token: Set header `Authorization: Bearer <access_token>`

---

## 🔍 API Endpoints

| Endpoint                     | Method | Description                       | Role     |
|-----------------------------|--------|-----------------------------------|----------|
| `/api/token/`               | POST   | Get access & refresh token        | All users |
| `/api/admin/tickets/`       | POST   | Create a ticket                   | Admin    |
| `/api/agent/fetch-tickets/` | GET    | Agent fetches up to 15 tickets    | Agent    |
| `/api/agent/sell-ticket/<id>/` | POST | Sell a ticket with customer info | Agent    |

For full endpoints check attached postman configs
---

## 🧪 Running Tests

```bash
python manage.py test tickets
```

This includes:
- CRUD and permission tests
- Agent ticket assignment
- Threaded concurrency test with `TransactionTestCase`

---

## ✍️ Author

**Khaled Elrefaey**  
> Backend developer & Python enthusiast

📫 Contact: [alzekarey@gmail.com]

---
