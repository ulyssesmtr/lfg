#!/bin/bash

# Wait for postgresql to accept connections
bash -c 'while !</dev/tcp/db/5432; do sleep 1; done;'

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Create initial form fields
echo "Loading initial data"
python manage.py loaddata loan_field_fixture.json

# Create superuser
echo "Creating admin user"
python manage.py createsuperuser --noinput

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000

