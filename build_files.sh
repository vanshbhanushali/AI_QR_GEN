#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure pip is available for python3.12 and upgrade it
echo "Ensuring pip for Python 3.12..."
python3.12 -m ensurepip
python3.12 -m pip install --upgrade pip

# Install dependencies using the specific python3.12 pip module
echo "Installing requirements..."
python3.12 -m pip install -r requirements.txt

# Test google.generativeai import
echo "Testing google.generativeai import..."
python3.12 -c "import google.generativeai" 
echo "Import test successful."

# Run database migrations using python3.12
echo "Running migrations..."
python3.12 manage.py migrate

# Collect static files using python3.12
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

echo "Build script finished successfully."