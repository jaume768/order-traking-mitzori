# Migrations Folder

This folder contains Django database migrations for the `orders` app.

**IMPORTANT**: Do not delete this folder or the `__init__.py` file. They are required for the application to work correctly.

## Files

- `__init__.py` - Required Python package marker
- `0001_initial.py` - Initial database schema for Order and OrderHistory models

## Creating New Migrations

When you modify models in `orders/models.py`, create new migrations:

```bash
# Inside Docker container
docker exec -it pedidos_backend python manage.py makemigrations orders

# Apply migrations
docker exec -it pedidos_backend python manage.py migrate orders
```

## Resetting Migrations

If you need to reset the database (development only):

```bash
docker-compose down -v
docker-compose up --build
```
