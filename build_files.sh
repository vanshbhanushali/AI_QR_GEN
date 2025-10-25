#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "Installing requirements..."
python -m pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build script finished successfully."