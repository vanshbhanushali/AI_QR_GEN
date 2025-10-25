#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure pip is available for python3.10 and upgrade it
echo "Ensuring pip for Python 3.10..."
python3.10 -m ensurepip
python3.10 -m pip install --upgrade pip

# Install dependencies using the specific python3.10 pip module
echo "Installing requirements..."
python3.10 -m pip install -r requirements.txt

# Run database migrations using python3.10
echo "Running migrations..."
python3.10 manage.py migrate

# Collect static files using python3.10
echo "Collecting static files..."
python3.10 manage.py collectstatic --noinput --clear

echo "Build script finished successfully."