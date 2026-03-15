#!/bin/bash
set -e

echo "==> Creando directorios necesarios..."
mkdir -p logs media

echo "==> Aplicando migraciones..."
python manage.py migrate --noinput

echo "==> Cargando datos iniciales..."
python manage.py loaddata control/fixtures/empleados.json 2>/dev/null \
  && echo "Fixtures cargados." \
  || echo "Fixtures ya existentes o error ignorado."

echo "==> Creando usuario admin..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@reportes.com', '123456')
    print('Usuario admin creado.')
else:
    print('Usuario admin ya existe.')
"

echo "==> Verificando integridad de DB..."
python manage.py verificar_db || true

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> Iniciando servidor en puerto ${PORT:-8000}..."
exec gunicorn asistencia.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
