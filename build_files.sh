#!/bin/bash

# Install dependencies using python3.10's pip module
python3.10 -m pip install -r requirements.txt 

# Run database migrations using python3.10
python3.10 manage.py migrate

# Collect static files using python3.10
python3.10 manage.py collectstatic --noinput --clear