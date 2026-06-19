# Ecommerce-WebApp

![Python](https://img.shields.io/badge/python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/django-5.1-green?logo=django)
![DRF](https://img.shields.io/badge/django--rest--framework-3.15-red)
![Stripe](https://img.shields.io/badge/stripe-integrated-626CD9?logo=stripe)
![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-yellow)

A production-grade e-commerce backend built with Django & Django REST Framework. Features product management, shopping cart, order processing, Stripe payment integration, JWT authentication, Celery async task queueing, and ML-powered product recommendations.

---

## Features

- **Product Management** – CRUD for products, collections, categories with nested images
- **Shopping Cart** – Add / update / remove items, session-based cart, guest carts
- **Order Processing** – Place orders from cart, payment status tracking, order history
- **Stripe Payments** – Checkout session creation, redirect to Stripe, webhook-ready
- **JWT Authentication** – Token-based auth via Djoser + SimpleJWT
- **Search & Filter** – Full-text search on title/description, filter by collection/price range, ordering
- **Pagination** – Page-based pagination (10 per page default)
- **Permissions** – Admin-only write, authenticated read, custom granular permissions
- **Celery Async Tasks** – Background email notifications, scheduled tasks with Celery Beat
- **ML Recommendations** – TF-IDF + cosine similarity for "products you may like"
- **Redis Caching** – Django Redis cache backend for recommendations and sessions
- **Testing** – pytest + pytest-django + model-bakery for robust test coverage

---

## Tech Stack

| Layer      | Technology                                                   |
| ---------- | ------------------------------------------------------------ |
| Framework  | Django 5.1, Django REST Framework 3.15                       |
| Auth       | Djoser, SimpleJWT (JWT)                                      |
| Database   | MySQL (dev), SQLite (CI)                                     |
| Cache / Queue | Redis, Celery, Celery Beat, Flower                        |
| Payments   | Stripe Checkout Sessions                                     |
| ML         | scikit-learn (TF-IDF, cosine similarity), pandas, numpy      |
| Testing    | pytest, pytest-django, model-bakery, locust                  |
| Tooling    | pipenv, django-filter, drf-nested-routers, whitenoise, silk  |

---

## Project Structure

```
Ecommerce-WebApp/
├── core/                  # User model, checkout views, Stripe integration
│   ├── models.py
│   ├── serializers.py
│   ├── views.py           # start_checkout, success
│   ├── urls.py
│   ├── signals/
│   └── templates/
├── djangowork/            # Django project root (settings, urls, wsgi, asgi)
│   ├── settings/
│   │   ├── common.py      # Shared settings
│   │   ├── dev.py         # Development (MySQL, Redis, debug)
│   │   └── prod.py        # Production (placeholder)
│   ├── celery.py          # Celery app
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/                 # Main e-commerce app
│   ├── models.py          # Product, Collection, Cart, Order, Review, etc.
│   ├── serializers.py
│   ├── views.py           # ViewSets for all resources
│   ├── urls.py            # Nested routers
│   ├── filters.py         # ProductFilter (collection, price range)
│   ├── pagination.py      # DefaultPagination (page_size=10)
│   ├── permissions.py     # IsAdminorReadOnly, ViewCustomerHistoryPermission
│   ├── recommendation.py  # TF-IDF + cosine similarity recommendations
│   ├── validators.py
│   ├── signals/           # Auto-create Customer on User signup
│   ├── management/        # seed_db management command
│   └── tests/             # pytest test suite
├── playground/            # Celery tasks, sample templates
│   ├── tasks.py           # notify_customer async task
│   └── ...
├── likes/                 # Likes app (generic likes)
├── tags/                  # Tags app (generic tagging)
├── manage.py
├── Pipfile / Pipfile.lock
├── pytest.ini
└── .gitignore
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mdahmedking6/Ecommerce-WebApp.git
cd Ecommerce-WebApp

# Install dependencies (including dev)
pipenv install --dev

# Activate the virtual environment
pipenv shell

# Run migrations
pipenv run python manage.py migrate

# Start the development server
pipenv run python manage.py runserver
```

> **Note:** Development requires MySQL and Redis running locally.  
> For a quick CI-style setup, set `DB_ENGINE=django.db.backends.sqlite3` and skip Redis.

---

## API Documentation

All endpoints are prefixed with `/store/` unless noted otherwise.

| Method | Endpoint                          | Description                      |
| ------ | --------------------------------- | -------------------------------- |
| GET    | `/store/product/`                 | List products (paginated, filterable) |
| POST   | `/store/product/`                 | Create product (admin)           |
| GET    | `/store/product/{id}/`            | Product detail                   |
| PUT    | `/store/product/{id}/`            | Update product (admin)           |
| DELETE | `/store/product/{id}/`            | Delete product (admin)           |
| GET    | `/store/product/{id}/review/`     | List product reviews             |
| POST   | `/store/product/{id}/review/`     | Create review                    |
| GET    | `/store/product/{id}/images/`     | List product images              |
| POST   | `/store/product/{id}/images/`     | Upload product image             |
| GET    | `/store/product/{id}/recommendations/` | ML-based similar products  |
| GET    | `/store/collection/`              | List collections                 |
| POST   | `/store/collection/`              | Create collection (admin)        |
| GET    | `/store/collection/{id}/`         | Collection detail                |
| PUT    | `/store/collection/{id}/`         | Update collection (admin)        |
| DELETE | `/store/collection/{id}/`         | Delete collection (admin)        |
| GET    | `/store/carts/`                   | List carts (authenticated)       |
| POST   | `/store/carts/`                   | Create cart                      |
| GET    | `/store/carts/{id}/`              | Cart detail with items           |
| DELETE | `/store/carts/{id}/`              | Delete cart                      |
| GET    | `/store/carts/{id}/items/`        | List cart items                  |
| POST   | `/store/carts/{id}/items/`        | Add item to cart                 |
| PATCH  | `/store/carts/{id}/items/{item_id}/` | Update item quantity         |
| DELETE | `/store/carts/{id}/items/{item_id}/` | Remove item from cart       |
| GET    | `/store/orders/`                  | List orders (own or all if staff) |
| POST   | `/store/orders/`                  | Create order from cart           |
| GET    | `/store/orders/{id}/`             | Order detail                     |
| PATCH  | `/store/orders/{id}/`             | Update order payment status (admin) |
| GET    | `/store/customer/me/`             | Current user's profile           |
| PUT    | `/store/customer/me/`             | Update profile                   |
| GET    | `/store/customer/{id}/history/`   | Customer order history           |
| POST   | `/core/checkout/{cart_id}/start/` | Stripe checkout session          |
| POST   | `/auth/users/`                    | Register (Djoser)                |
| POST   | `/auth/jwt/create/`               | Obtain JWT                       |
| POST   | `/auth/jwt/refresh/`              | Refresh JWT                      |

---

## Testing

```bash
# Run all tests with pytest
pipenv run python -m pytest

# Run with coverage
pipenv run python -m pytest --cov

# Watch mode (auto-re-run on changes)
pipenv run ptw
```

Tests are located in `store/tests/` and use `pytest-django` with `model-bakery` for fixtures.  
The test configuration is in `pytest.ini` (`DJANGO_SETTINGS_MODULE=djangowork.settings.dev`).

---

## Environment Variables

Create a `.env` file in the project root (see `.env.example`):

| Variable            | Description                         |
| ------------------- | ----------------------------------- |
| `SECRET_KEY`        | Django secret key (prod only)       |
| `DB_ENGINE`         | Database engine (e.g. `django.db.backends.mysql`) |
| `DB_NAME`           | Database name                       |
| `DB_USER`           | Database user                       |
| `DB_PASS`           | Database password                   |
| `DB_HOST`           | Database host                       |
| `DB_PORT`           | Database port                       |
| `STRIPE_SECRET_KEY` | Stripe secret key (sk_test_...)     |
| `EMAIL_HOST`        | SMTP host                           |
| `EMAIL_PORT`        | SMTP port                           |
| `DEFAULT_FROM_EMAIL`| Default sender email                |
| `DJANGO_LOG_LEVEL`  | Logging level (default: INFO)       |

---

## Docker

```bash
# Build and run with Docker Compose
docker compose up --build
```

> A `Dockerfile` and `docker-compose.yml` will be added soon.  
> For now, follow the Quick Start instructions above.

---

## License

[MIT](LICENSE) Copyright (c) 2025 Mohammed Ahmed Anjarwala
