#!/bin/bash

# Install dependencies using the environment's pip
python -m pip install -r requirements.txt 

# Run database migrations using the environment's python
python manage.py migrate

# Collect static files using the environment's python
python manage.py collectstatic --noinput --clear