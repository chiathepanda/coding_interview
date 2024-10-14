#!/bin/bash

set -e

DB_PORT=${DATABASE_PORT:-5432} 
DB_HOST=${DATABASE_HOST:-db}

python manage.py collectstatic --noinput
# Wait for the database
echo "Waiting for database"
while ! nc -z $DB_HOST $DB_PORT; do
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