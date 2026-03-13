#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting application..."
# This 'exec "$@"' runs the CMD from the Dockerfile (Gunicorn)
exec "$@"