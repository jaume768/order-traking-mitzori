#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe (SOLO PRIMERA VEZ - luego comenta esto)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mitzori.com', 'CAMBIAR_ESTA_CONTRASEÑA')" | python manage.py shell

echo "Iniciando Gunicorn..."
# Iniciar Gunicorn
exec "$@"
