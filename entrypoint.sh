#!/bin/sh

# Optional: Wait for database to be ready
# (Useful if the DB pod is still booting)
echo "Waiting for postgres..."
# You can add a 'sleep' or a 'nc' check here if needed

echo "Running migrations..."
python manage.py migrate --noinput

