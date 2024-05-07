#!/bin/bash

# Aplicar migraciones de Django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput

# Iniciar el servidor de Django
exec "$@"