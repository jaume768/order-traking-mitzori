# 🛠️ Comandos Útiles

## Docker Commands

### Iniciar servicios
```bash
# Iniciar todos los servicios
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Reconstruir e iniciar
docker-compose up --build
```

### Detener servicios
```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (limpieza completa)
docker-compose down -v
```

### Ver logs
```bash
# Ver todos los logs
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Seguir logs en tiempo real
docker-compose logs -f backend
```

### Ejecutar comandos en contenedores
```bash
# Acceder al shell del backend
docker-compose exec backend bash

# Ejecutar comandos Django
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py shell

# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d pedidos_db
```

---

## Django Commands (Backend)

### Migraciones
```bash
# Activar venv primero
cd backend
venv\Scripts\activate

# Crear migraciones para todas las apps
python manage.py makemigrations

# Crear migraciones para una app específica
python manage.py makemigrations orders

# Aplicar migraciones
python manage.py migrate

# Aplicar migraciones de una app específica
python manage.py migrate orders

# Ver estado de migraciones
python manage.py showmigrations
```

**IMPORTANTE**: Las migraciones ya están incluidas en el proyecto en `backend/orders/migrations/`. No las elimines.

### Administración
```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña de usuario
python manage.py changepassword admin

# Recopilar archivos estáticos
python manage.py collectstatic
```

### Base de datos
```bash
# Abrir shell de Django
python manage.py shell

# Vaciar base de datos (cuidado!)
python manage.py flush

# Exportar datos
python manage.py dumpdata orders > backup.json

# Importar datos
python manage.py loaddata backup.json
```

### Servidor de desarrollo
```bash
# Iniciar servidor
python manage.py runserver

# Iniciar en puerto específico
python manage.py runserver 8080

# Permitir acceso externo
python manage.py runserver 0.0.0.0:8000
```

---

## Next.js Commands (Frontend)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build

# Iniciar servidor de producción
npm start

# Limpiar cache de Next.js
Remove-Item -Recurse -Force .next
```

---

## PostgreSQL Commands

### Dentro del contenedor Docker
```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d pedidos_db

# Una vez dentro:
\dt                    # Listar tablas
\d orders_order        # Describir tabla
SELECT * FROM orders_order;
\q                     # Salir
```

### Backup y Restore
```bash
# Backup
docker-compose exec -T db pg_dump -U postgres pedidos_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres pedidos_db < backup.sql
```

---

## Git Commands

```bash
# Inicializar repositorio
git init

# Añadir archivos
git add .

# Commit
git commit -m "Initial commit: Sistema de seguimiento de pedidos"

# Añadir remote
git remote add origin <url-del-repo>

# Push
git push -u origin main
```

---

## Limpieza y Mantenimiento

### Limpiar Docker
```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes no usadas
docker image prune

# Eliminar volúmenes no usados
docker volume prune

# Limpieza completa (cuidado!)
docker system prune -a --volumes
```

### Limpiar archivos temporales
```bash
# Backend - eliminar __pycache__
cd backend
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Frontend - eliminar node_modules y .next
cd frontend
Remove-Item -Recurse -Force node_modules, .next
```

---

## Verificación de Estado

### Verificar que todo funciona
```bash
# Ver contenedores corriendo
docker-compose ps

# Verificar salud de la BD
docker-compose exec db pg_isready -U postgres

# Test del backend
curl http://localhost:8000/admin/

# Test del frontend
curl http://localhost:3000/
```

### Ver uso de recursos
```bash
# Ver estadísticas de contenedores
docker stats

# Ver espacio usado
docker system df
```

---

## Desarrollo y Testing

### Crear datos de prueba (Django Shell)
```bash
docker-compose exec backend python manage.py shell
```

```python
from orders.models import Order, OrderHistory
from django.utils import timezone

# Crear pedido de prueba
order = Order.objects.create(
    order_number="TEST001",
    customer_name="Cliente de Prueba",
    customer_email="test@example.com",
    delivery_address="Calle Falsa 123",
    delivery_city="Madrid",
    delivery_postal_code="28001",
    status="IN_TRANSIT",
    current_location="Centro de Distribución Madrid",
    estimated_delivery=timezone.now() + timezone.timedelta(days=2)
)

# Crear historial
OrderHistory.objects.create(
    order=order,
    status="PENDING",
    location="Almacén Central",
    description="Pedido recibido"
)

print(f"Pedido creado: {order.order_number}")
```

---

## Troubleshooting

### Puerto ya en uso
```bash
# Ver qué usa el puerto 8000
netstat -ano | findstr :8000

# Matar proceso (usar PID del comando anterior)
taskkill /PID <PID> /F
```

### Resetear todo el proyecto
```bash
# 1. Detener y limpiar Docker
docker-compose down -v

# 2. Eliminar bases de datos locales
cd backend
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue

# 3. Eliminar migraciones (excepto __init__.py)
Get-ChildItem -Path orders/migrations -Exclude __init__.py | Remove-Item

# 4. Reconstruir
docker-compose up --build
```

---

## Variables de Entorno

### Backend (.env)
```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
DATABASE_NAME=pedidos_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

¿Necesitas más ayuda? Revisa el [README.md](README.md) o la [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
