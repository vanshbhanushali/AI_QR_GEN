#!/bin/bash

# Install dependencies using pip3
pip3 install -r requirements.txt 

# Run database migrations using python3.9
python3.9 manage.py migrate

# Collect static files using python3.9
python3.9 manage.py collectstatic --noinput --clear