saloon-master/
├── backend/
│   ├── app/
│   │   ├── __init__.py         # Flask app factory
│   │   ├── config.py           # Configuration settings
│   │   ├── models/             # Data interaction layer (wrappers around pymongo)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── shop.py
│   │   │   ├── worker.py
│   │   │   ├── booking.py
│   │   │   └── review.py
│   │   ├── schemas/            # Marshmallow schemas for validation/serialization
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── shop.py
│   │   │   ├── worker.py
│   │   │   ├── booking.py
│   │   │   └── review.py
│   │   ├── routes/             # API Blueprints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py        # Includes Admin user management
│   │   │   ├── shops.py        # Includes Owner registration, Customer discovery
│   │   │   ├── bookings.py     # Customer booking, Owner management
│   │   │   ├── workers.py      # Owner worker management
│   │   │   ├── reviews.py
│   │   │   ├── analytics.py    # Owner/Admin dashboards
│   │   │   ├── notifications.py # Placeholder
│   │   │   └── chat.py         # Placeholder
│   │   ├── services/           # Business logic (optional, good practice)
│   │   │   ├── email_service.py # Mock email
│   │   │   └── payment_service.py # Mock payment
│   │   ├── utils/              # Helper functions, decorators
│   │   │   ├── __init__.py
│   │   │   ├── security.py     # JWT helpers, RBAC decorators, hashing
│   │   │   └── helpers.py      # Generic utilities
│   │   └── extensions.py       # Flask extension initializations (db, jwt, bcrypt, cors, ma)
│   ├── run.py                  # Application entry point
│   ├── requirements.txt        # Backend dependencies
│   └── .env.example            # Environment variable template