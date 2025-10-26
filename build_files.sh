#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Ensure pip is available for python3.9 and upgrade it
echo "Ensuring pip for Python 3.9..."
python3.9 -m ensurepip
python3.9 -m pip install --upgrade pip

# Install dependencies using the specific python3.9 pip module
echo "Installing requirements..."
python3.9 -m pip install -r requirements.txt

# Test google.generativeai import
echo "Testing google.generativeai import..."
python3.9 -c "import google.generativeai" 
echo "Import test successful."

# Run database migrations using python3.9
echo "Running migrations..."
python3.9 manage.py migrate

# Collect static files using python3.9
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

echo "Build script finished successfully."