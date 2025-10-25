@echo off
echo ===================================
echo Configuracion de Desarrollo Local
echo ===================================
echo.

echo [1/4] Configurando Backend Django...
cd backend

echo Creando entorno virtual...
python -m venv venv

echo Activando entorno virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Backend configurado!
echo Para activar el entorno virtual usa: backend\venv\Scripts\activate
echo.

cd ..

echo [2/4] Configurando Frontend Next.js...
cd frontend

echo Instalando dependencias de Node...
call npm install

echo.
echo Frontend configurado!
echo.

cd ..

echo [3/4] Copiando archivos de configuracion...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo Archivo backend\.env creado
)

if not exist frontend\.env.local (
    copy frontend\.env.local.example frontend\.env.local
    echo Archivo frontend\.env.local creado
)

echo.
echo [4/4] Configuracion completada!
echo.
echo ===================================
echo Proximos pasos:
echo ===================================
echo.
echo Para desarrollo con Docker:
echo   - Ejecuta: start.bat
echo.
echo Para desarrollo local:
echo   1. Backend: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo   2. Frontend: cd frontend ^&^& npm run dev
echo.
echo Accede a:
echo   - Frontend: http://localhost:3000
echo   - Backend Admin: http://localhost:8000/admin
echo.

pause
