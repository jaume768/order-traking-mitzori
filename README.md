# 📦 Sistema de Seguimiento de Pedidos - Mitzori

Sistema completo de seguimiento de pedidos con Next.js (frontend), Django (backend/API REST/admin) y PostgreSQL, todo containerizado con Docker.

## 🚀 Características

- **Frontend Next.js**: Interfaz moderna con JavaScript y CSS puro para que los usuarios rastreen sus pedidos
- **Backend Django**: API REST completa y panel de administración para gestionar pedidos
- **Base de datos PostgreSQL**: Almacenamiento robusto y confiable
- **Docker**: Todo containerizado para fácil despliegue y desarrollo
- **Seguimiento en tiempo real**: Barra de progreso visual y historial completo
- **Panel Admin**: Interfaz visual con badges de colores y barras de progreso

## 📋 Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Git (opcional, para clonar el repositorio)

## 🛠️ Instalación y Configuración

### 1. Clonar o navegar al proyecto

```bash
cd c:\Users\jaume\OneDrive\Imágenes\Escritorio\Proyectos\UbicacionPedidoMitzori
```

### 2. Configurar variables de entorno

#### Backend (.env)
Copia el archivo de ejemplo y ajusta según necesites:

```bash
copy backend\.env.example backend\.env
```

#### Frontend (.env.local)
```bash
copy frontend\.env.local.example frontend\.env.local
```

### 3. Construir e iniciar los contenedores

```bash
docker-compose up --build
```

Esto iniciará:
- **PostgreSQL**: `localhost:5432`
- **Django Backend**: `http://localhost:8000`
- **Next.js Frontend**: `http://localhost:3000`

**Nota**: Las migraciones de Django se aplican automáticamente al iniciar el contenedor.

### 4. Crear superusuario (primera vez)

El sistema crea automáticamente un usuario admin, pero puedes crear el tuyo:

```bash
docker exec -it pedidos_backend python manage.py createsuperuser
```

### 5. Acceder a la aplicación

- **Frontend (usuarios)**: http://localhost:3000
- **Backend Admin**: http://localhost:8000/admin
  - Usuario: `admin` (creado automáticamente)
  - Contraseña: `admin123`
- **API REST**: http://localhost:8000/api/

## 🔧 Desarrollo Local (sin Docker)

### Backend Django

1. **Crear y activar entorno virtual**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos** (asegúrate de tener PostgreSQL corriendo):
```bash
# Crea la base de datos 'pedidos_db' en PostgreSQL
# Actualiza las credenciales en backend/.env
```

4. **Aplicar migraciones**:
```bash
python manage.py migrate
```

5. **Crear superusuario**:
```bash
python manage.py createsuperuser
```

6. **Iniciar servidor**:
```bash
python manage.py runserver
```

### Frontend Next.js

1. **Instalar dependencias**:
```bash
cd frontend
npm install
```

2. **Configurar variables de entorno**:
```bash
# Crear archivo .env.local
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local
```

3. **Iniciar servidor de desarrollo**:
```bash
npm run dev
```

## 📚 Uso del Sistema

### Para Usuarios (Frontend)

1. Accede a http://localhost:3000
2. Ingresa tu número de pedido en el campo de búsqueda
3. Visualiza el estado actual, progreso y historial de tu pedido

### Para Administradores (Backend Admin)

1. Accede a http://localhost:8000/admin
2. Inicia sesión con tus credenciales
3. Gestiona pedidos desde el panel:
   - **Crear nuevo pedido**: Click en "Añadir Pedido"
   - **Actualizar estado**: Edita el pedido y cambia el estado
   - **Ver historial**: Cada cambio se registra automáticamente

#### Estados de Pedido

- **Pedido Recibido**: Pedido creado en el sistema
- **En Preparación**: Preparando el pedido para envío
- **Enviado**: Pedido enviado desde el almacén
- **En Tránsito**: Pedido en camino
- **En Reparto**: Pedido en ruta de entrega final
- **Entregado**: Pedido entregado exitosamente
- **Cancelado**: Pedido cancelado

## 🔌 Endpoints API

### Buscar Pedido
```http
POST /api/orders/search/
Content-Type: application/json

{
  "order_number": "ABC123"
}
```

### Rastrear Pedido (GET)
```http
GET /api/orders/track/{order_number}/
```

**Respuesta**:
```json
{
  "order_number": "ABC123",
  "status": "IN_TRANSIT",
  "status_display": "En Tránsito",
  "current_location": "Centro de Distribución Madrid",
  "progress_percentage": 60,
  "estimated_delivery": "2025-10-27T15:00:00Z",
  "delivered_at": null,
  "history": [
    {
      "status_display": "En Tránsito",
      "location": "Centro de Distribución Madrid",
      "description": "Estado actualizado a En Tránsito",
      "timestamp": "2025-10-25T10:30:00Z"
    }
  ]
}
```

## 📁 Estructura del Proyecto

```
UbicacionPedidoMitzori/
├── backend/                    # Django Backend
│   ├── config/                 # Configuración Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── orders/                 # App de pedidos
│   │   ├── models.py          # Modelos Order y OrderHistory
│   │   ├── views.py           # ViewSets API
│   │   ├── serializers.py     # Serializers REST
│   │   ├── admin.py           # Configuración admin
│   │   └── urls.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App Router
│   │   │   ├── layout.js
│   │   │   ├── page.js
│   │   │   └── globals.css
│   │   ├── components/        # Componentes React
│   │   │   └── OrderTracker.js
│   │   └── lib/               # Utilidades
│   │       └── api.js
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── .env.local.example
├── docker-compose.yml
└── README.md
```

## 🐛 Solución de Problemas

### El contenedor de backend no inicia

1. Verifica que PostgreSQL esté corriendo:
```bash
docker-compose ps
```

2. Revisa los logs:
```bash
docker-compose logs backend
```

3. Reconstruye los contenedores:
```bash
docker-compose down -v
docker-compose up --build
```

### No puedo acceder al admin de Django

1. Asegúrate de que el backend esté corriendo
2. El superusuario se crea automáticamente:
   - Usuario: `admin`
   - Contraseña: `admin123`
3. Si necesitas crear uno nuevo:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### El frontend no se conecta al backend

1. Verifica las variables de entorno en `frontend/.env.local`
2. Asegúrate de que el backend esté en el puerto 8000
3. Revisa la configuración de CORS en `backend/config/settings.py`

## 🚀 Despliegue en Producción

Para desplegar en AWS con SSL automático, consulta la guía completa:

**[📖 Ver Guía de Despliegue en AWS](DESPLIEGUE_AWS.md)**

### Resumen rápido:

1. **Instancia EC2** con Ubuntu 22.04
2. **DNS configurado**: `orders.mitzori.com` → IP de tu EC2
3. **Puertos abiertos**: 80, 443, 22
4. **Despliegue con un comando**:
   ```bash
   ./deploy.sh
   ```

### Acceso en producción:
- **Frontend**: https://orders.mitzori.com
- **Admin**: https://orders.mitzori.com/admin
- **API**: https://orders.mitzori.com/api

Caddy gestiona automáticamente los certificados SSL con Let's Encrypt.

## 🔒 Seguridad

✅ **SSL automático** con Caddy y Let's Encrypt  
✅ **HTTPS forzado** con redirección automática  
✅ **Headers de seguridad** (HSTS, X-Frame-Options, etc.)  
✅ **Gunicorn** para servir Django en producción  
✅ **Variables de entorno** separadas para dev/prod  
✅ **Usuario no-root** en contenedores

## 📝 Licencia

Este proyecto es privado y confidencial.

## 👥 Contacto

Para soporte o preguntas, contacta al equipo de desarrollo.

---

**¡Desarrollado con ❤️ para Mitzori!**
