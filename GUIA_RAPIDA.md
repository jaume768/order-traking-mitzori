# 🚀 Guía Rápida de Inicio

## Opción 1: Usar Docker (Recomendado)

### Paso 1: Configurar variables de entorno
```bash
# Copia los archivos de ejemplo
copy backend\.env.example backend\.env
copy frontend\.env.local.example frontend\.env.local
```

### Paso 2: Iniciar la aplicación
```bash
# Simplemente ejecuta:
start.bat

# O manualmente:
docker-compose up --build
```

**Importante**: La primera vez puede tardar unos minutos mientras se construyen las imágenes y se aplican las migraciones.

### Paso 3: Crear superusuario (primera instalación)

El sistema intenta crear un usuario automáticamente, pero si no funciona:

```bash
docker exec -it pedidos_backend python manage.py createsuperuser
```

### Paso 4: Acceder
- **Frontend**: http://localhost:3000
- **Admin Django**: http://localhost:8000/admin
  - Usuario: `admin` (o el que creaste)
  - Contraseña: `admin123` (o la que configuraste)

---

## Opción 2: Desarrollo Local (con venv)

### Configuración Automática
```bash
# Ejecuta el script de configuración:
setup-dev.bat
```

### Configuración Manual

#### Backend Django
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configura el archivo .env con tus credenciales de PostgreSQL
# Asegúrate de tener PostgreSQL corriendo localmente

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend Next.js
```bash
cd frontend
npm install

# Crea .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

npm run dev
```

---

## 📝 Crear tu primer pedido

1. Ve a http://localhost:8000/admin
2. Inicia sesión con `admin` / `admin123`
3. Click en "Pedidos" → "Añadir Pedido"
4. Completa:
   - **Número de Pedido**: Por ejemplo `PED001`
   - **Nombre del Cliente**: Tu nombre
   - **Dirección de Entrega**: Una dirección
   - **Ciudad**: Tu ciudad
   - **Código Postal**: Tu CP
   - **Estado**: Selecciona "Pedido Recibido"
5. Guarda el pedido
6. Ve a http://localhost:3000 y busca el pedido `PED001`

---

## 🔄 Actualizar estado de un pedido

1. En el admin, edita el pedido
2. Cambia el **Estado** (por ejemplo, a "En Preparación")
3. Opcionalmente actualiza **Ubicación Actual**
4. Guarda
5. El historial se actualiza automáticamente
6. Refresca la página del frontend para ver los cambios

---

## 🛑 Detener la aplicación

### Con Docker
```bash
# Ejecuta:
stop.bat

# O manualmente:
docker-compose down
```

### Sin Docker
- Presiona `Ctrl+C` en cada terminal donde corre el backend/frontend

---

## ✅ Estados disponibles

- **Pedido Recibido** (0%) - Pedido creado
- **En Preparación** (20%) - Preparando el envío
- **Enviado** (40%) - Salió del almacén
- **En Tránsito** (60%) - En camino
- **En Reparto** (80%) - En ruta de entrega
- **Entregado** (100%) - ¡Completado!
- **Cancelado** (0%) - Pedido cancelado

---

## 🐛 Problemas comunes

### Docker no inicia
- Asegúrate de que Docker Desktop esté ejecutándose
- Verifica que los puertos 3000, 8000 y 5432 estén libres

### Error de base de datos
```bash
# Elimina los volúmenes y recrea:
docker-compose down -v
docker-compose up --build
```

### El frontend no muestra datos
- Verifica que el backend esté corriendo en el puerto 8000
- Revisa el archivo `.env.local` del frontend
- Abre la consola del navegador para ver errores

---

¡Listo! Ya puedes empezar a usar el sistema de seguimiento de pedidos. 🎉
