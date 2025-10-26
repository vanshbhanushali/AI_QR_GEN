#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure pip is available for python3.11 and upgrade it
echo "Ensuring pip for Python 3.11..."
python3.11 -m ensurepip
python3.11 -m pip install --upgrade pip

# Install dependencies using the specific python3.11 pip module
echo "Installing requirements..."
python3.11 -m pip install -r requirements.txt

# Test google.generativeai import
echo "Testing google.generativeai import..."
python3.11 -c "import google.generativeai" 
echo "Import test successful."

# Run database migrations using python3.11
echo "Running migrations..."
python3.11 manage.py migrate

# Collect static files using python3.11
echo "Collecting static files..."
python3.11 manage.py collectstatic --noinput --clear

echo "Build script finished successfully."