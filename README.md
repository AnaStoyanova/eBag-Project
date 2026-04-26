# eCommerce Product Service

A REST API for managing products and categories in an e-commerce system.

## Stack

- Python 3.9 / Django 4.2 / Django REST Framework
- PostgreSQL
- django-filter, django-mptt, drf-spectacular

## Setup

```bash
brew services start postgresql@18
psql postgres -c "CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_pass';"
psql postgres -c "CREATE DATABASE ecommerce_db OWNER ecommerce_user;"
psql postgres -c "ALTER USER ecommerce_user CREATEDB;"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
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

### Pagination

List endpoints return paginated results (20 per page by default). Use `?page_size=N` to override (max 100).

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Validation

- `price` must be greater than zero
- `sku` may only contain letters, numbers, and hyphens — automatically uppercased

## Docs

Interactive API docs: `http://localhost:8000/api/docs/`

## Tests

```bash
python manage.py test products
```
