#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure pip is available for the active python and upgrade it
echo "Ensuring pip for Python..."
python -m ensurepip
python -m pip install --upgrade pip

# Install dependencies using the active python pip module
echo "Installing requirements..."
python -m pip install -r requirements.txt

# Run database migrations using the active python
echo "Running migrations..."
python manage.py migrate

# Collect static files using the active python
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build script finished successfully."