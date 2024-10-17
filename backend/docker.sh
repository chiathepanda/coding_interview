#!/bin/bash

set -e

DB_PORT=${DATABASE_PORT:-3306} 
DB_HOST=${DATABASE_HOST:-db}

python manage.py collectstatic --noinput

# Wait for the database service to be ready
echo "Waiting for database"
MAX_TRIES=60
TRIES=0
while ! mysqladmin ping -h"$DB_HOST" --silent; do
    TRIES=$((TRIES+1))
    if [ "$TRIES" -ge "$MAX_TRIES" ]; then
        echo "MySQL service not available.  exiting."
        exit 1
    fi
    sleep 1
done

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# populate with dummy data
python manage.py populate_db

# Check the DJANGO_ENV environment variable to determine the server
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Starting Gunicorn (Production)..."
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000
else
    echo "Starting Django Development Server..."
    python manage.py runserver 0.0.0.0:8000
fi