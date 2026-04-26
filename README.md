# eCommerce Product Service

A REST API for managing products and categories in an e-commerce system.

## Stack

- Python 3.9 / Django 4.2 / Django REST Framework
- PostgreSQL
- django-filter, django-mptt

## Setup

```bash
brew services start postgresql@18
source venv/bin/activate
python manage.py runserver
```

## API

| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/api/products/` | List / create products |
| GET/PUT/PATCH/DELETE | `/api/products/{id}/` | Retrieve / update / delete |
| GET | `/api/products/search/` | Search and filter products |
| GET/POST | `/api/categories/` | List / create categories |
| GET/PUT/PATCH/DELETE | `/api/categories/{id}/` | Retrieve / update / delete |

### Search filters

`GET /api/products/search/?title=phone&price_min=100&price_max=800&category=1`

| Param | Description |
|-------|-------------|
| `title` | Case-insensitive substring |
| `sku` | Exact match |
| `price_min` / `price_max` | Price range |
| `category` | Category ID — includes subcategories |

## Docs

Interactive API docs: `http://localhost:8000/api/docs/`

## Tests

```bash
python manage.py test products
```
