#!/usr/bin/env bash
# Script de build para Render (Web Service del backend).
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data
