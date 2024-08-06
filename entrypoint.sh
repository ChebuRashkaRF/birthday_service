#!/bin/sh
# Применение миграций базы данных
python manage.py makemigrations
python manage.py migrate --noinput
exec "$@"