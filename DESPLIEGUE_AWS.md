# 🚀 Guía de Despliegue en AWS

Esta guía te ayudará a desplegar el sistema de seguimiento de pedidos en AWS con SSL automático usando Caddy.

## 📋 Requisitos Previos

1. **Instancia EC2** (recomendado: t3.small o superior)
   - Ubuntu 22.04 LTS
   - Mínimo 2GB RAM
   - 20GB de almacenamiento

2. **Dominio configurado**
   - Subdominio: `orders.mitzori.com`
   - Registro A apuntando a la IP pública de tu EC2

3. **Puertos abiertos en Security Group**
   - Puerto 80 (HTTP)
   - Puerto 443 (HTTPS)
   - Puerto 22 (SSH)

## 🔧 Instalación en el Servidor

### 1. Conectarse al servidor

```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

### 2. Instalar Docker y Docker Compose

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version

# Salir y volver a conectar para aplicar cambios
exit
```

### 3. Clonar/Subir el proyecto

```bash
# Opción A: Desde Git (recomendado)
git clone https://github.com/tu-usuario/UbicacionPedidoMitzori.git
cd UbicacionPedidoMitzori

# Opción B: Subir archivos con SCP
# Desde tu máquina local:
scp -i tu-clave.pem -r ./UbicacionPedidoMitzori ubuntu@tu-ip-publica:~/
```

### 4. Configurar variables de entorno

```bash
cd UbicacionPedidoMitzori

# Copiar el archivo de ejemplo
cp .env.prod.example .env.prod

# Editar con nano o vim
nano .env.prod
```

**Configuración del archivo `.env.prod`:**

```env
# Django
DEBUG=False
SECRET_KEY=TU_CLAVE_SUPER_SECRETA_AQUI_GENERALA_RANDOM
DATABASE_NAME=pedidos_prod
DATABASE_USER=pedidos_user
DATABASE_PASSWORD=UNA_CONTRASEÑA_MUY_SEGURA
ALLOWED_HOSTS=orders.mitzori.com
CORS_ALLOWED_ORIGINS=https://orders.mitzori.com

# Next.js
NEXT_PUBLIC_API_URL=https://orders.mitzori.com/api
NODE_ENV=production
```

**Generar SECRET_KEY segura:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Verificar DNS

Antes de continuar, verifica que el dominio apunte correctamente:

```bash
dig orders.mitzori.com +short
# Debe mostrar la IP pública de tu EC2
```

### 6. Desplegar la aplicación

```bash
# Dar permisos de ejecución al script
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh
```

**O manualmente:**

```bash
# Construir e iniciar
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 7. Crear superusuario de Django

```bash
docker exec -it pedidos_backend_prod python manage.py createsuperuser
```

Ingresa:
- Username: `admin` (o el que prefieras)
- Email: `admin@mitzori.com`
- Password: (elige una contraseña segura)

## 🔐 Acceso a la Aplicación

Una vez desplegado, accede a:

- **Frontend público**: https://orders.mitzori.com
- **Panel de Admin**: https://orders.mitzori.com/admin
- **API REST**: https://orders.mitzori.com/api

## 🔒 Seguridad SSL

Caddy automáticamente:
- ✅ Obtiene certificados SSL de Let's Encrypt
- ✅ Renueva los certificados automáticamente
- ✅ Redirige HTTP → HTTPS
- ✅ Habilita HTTP/2 y HTTP/3

**No necesitas configurar nada más**, Caddy se encarga de todo.

## 📊 Monitoreo y Mantenimiento

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose -f docker-compose.prod.yml logs -f

# Solo backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Solo frontend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Solo Caddy
docker-compose -f docker-compose.prod.yml logs -f caddy
```

### Ver estado de contenedores

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Reiniciar servicios

```bash
# Reiniciar todo
docker-compose -f docker-compose.prod.yml restart

# Reiniciar solo un servicio
docker-compose -f docker-compose.prod.yml restart backend
```

### Backup de la base de datos

```bash
# Crear backup
docker exec pedidos_db_prod pg_dump -U pedidos_user pedidos_prod > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i pedidos_db_prod psql -U pedidos_user pedidos_prod < backup_20250101.sql
```

## 🔄 Actualizar la aplicación

```bash
# 1. Obtener últimos cambios (si usas Git)
git pull origin main

# 2. Ejecutar script de deploy
./deploy.sh

# O manualmente:
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

## 🛠️ Comandos Útiles

### Ejecutar comandos de Django

```bash
# Migraciones
docker exec -it pedidos_backend_prod python manage.py migrate

# Crear migraciones
docker exec -it pedidos_backend_prod python manage.py makemigrations

# Recopilar archivos estáticos
docker exec -it pedidos_backend_prod python manage.py collectstatic --noinput

# Abrir shell de Django
docker exec -it pedidos_backend_prod python manage.py shell
```

### Acceder a la base de datos

```bash
docker exec -it pedidos_db_prod psql -U pedidos_user pedidos_prod
```

### Limpiar Docker

```bash
# Eliminar imágenes no usadas
docker image prune -a

# Eliminar volúmenes no usados
docker volume prune

# Limpieza completa (¡cuidado!)
docker system prune -a --volumes
```

## 🔥 Troubleshooting

### SSL no funciona

1. Verifica que el dominio apunte a la IP correcta:
   ```bash
   dig orders.mitzori.com +short
   ```

2. Verifica logs de Caddy:
   ```bash
   docker-compose -f docker-compose.prod.yml logs caddy
   ```

3. Asegúrate que los puertos 80 y 443 estén abiertos en el Security Group de AWS

### Error 502 Bad Gateway

```bash
# Verificar que todos los servicios estén corriendo
docker-compose -f docker-compose.prod.yml ps

# Ver logs del backend
docker-compose -f docker-compose.prod.yml logs backend
```

### Base de datos no conecta

```bash
# Ver logs de la base de datos
docker-compose -f docker-compose.prod.yml logs db

# Verificar variables de entorno
docker-compose -f docker-compose.prod.yml config
```

## 📈 Optimizaciones de Producción

### 1. Configurar backups automáticos

Crea un cron job:

```bash
crontab -e

# Agregar (backup diario a las 2 AM):
0 2 * * * cd /home/ubuntu/UbicacionPedidoMitzori && docker exec pedidos_db_prod pg_dump -U pedidos_user pedidos_prod > /home/ubuntu/backups/backup_$(date +\%Y\%m\%d).sql
```

### 2. Configurar logrotate

```bash
sudo nano /etc/logrotate.d/docker-pedidos

# Agregar:
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
```

### 3. Monitoreo con AWS CloudWatch

Instala el agente de CloudWatch para monitorear:
- CPU
- Memoria
- Disco
- Logs de aplicación

## 🎯 Checklist de Despliegue

- [ ] Instancia EC2 creada y corriendo
- [ ] Docker y Docker Compose instalados
- [ ] DNS configurado (orders.mitzori.com → IP EC2)
- [ ] Security Group con puertos 80, 443, 22 abiertos
- [ ] `.env.prod` configurado con valores de producción
- [ ] SECRET_KEY generada aleatoriamente
- [ ] Contraseñas fuertes para DB y admin
- [ ] Aplicación desplegada con `./deploy.sh`
- [ ] SSL funcionando (https://)
- [ ] Superusuario creado
- [ ] Backup automático configurado
- [ ] Logs monitoreados

## 📞 Soporte

Si tienes problemas, revisa:
1. Logs de Docker: `docker-compose logs`
2. Estado de servicios: `docker-compose ps`
3. Conectividad: `curl https://orders.mitzori.com`

---

**¡Despliegue completado! 🎉**

Tu sistema de seguimiento de pedidos está ahora en producción con SSL automático.
