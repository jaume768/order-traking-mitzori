#!/bin/bash

# Script de despliegue para AWS
# Uso: ./deploy.sh

set -e

echo "=================================="
echo "Desplegando Sistema de Pedidos"
echo "=================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que existe .env.prod
if [ ! -f .env.prod ]; then
    echo -e "${RED}Error: .env.prod no encontrado${NC}"
    echo "Copia .env.prod.example a .env.prod y configúralo"
    exit 1
fi

# Hacer backup de la base de datos (si existe)
if docker ps | grep -q pedidos_db_prod; then
    echo -e "${YELLOW}Haciendo backup de la base de datos...${NC}"
    docker exec pedidos_db_prod pg_dump -U pedidos_user pedidos_prod > backup_$(date +%Y%m%d_%H%M%S).sql
fi

# Detener contenedores actuales
echo -e "${YELLOW}Deteniendo contenedores actuales...${NC}"
docker-compose -f docker-compose.prod.yml down

# Limpiar imágenes antiguas (opcional)
echo -e "${YELLOW}Limpiando imágenes antiguas...${NC}"
docker image prune -f

# Construir nuevas imágenes
echo -e "${YELLOW}Construyendo nuevas imágenes...${NC}"
docker-compose -f docker-compose.prod.yml build --no-cache

# Iniciar servicios
echo -e "${YELLOW}Iniciando servicios...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que los servicios estén listos
echo -e "${YELLOW}Esperando a que los servicios estén listos...${NC}"
sleep 10

# Verificar estado
echo -e "${GREEN}Verificando estado de los contenedores...${NC}"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo -e "${GREEN}=================================="
echo "Despliegue completado exitosamente"
echo "=================================="
echo ""
echo "Accede a:"
echo "  - Frontend: https://orders.mitzori.com"
echo "  - Admin: https://orders.mitzori.com/admin"
echo "  - API: https://orders.mitzori.com/api"
echo ""
echo "Para ver logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
