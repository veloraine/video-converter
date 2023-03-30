#!/usr/bin/env bash
echo 'Installing dependencies'
python3 pip install -r requirements.txt

echo 'Migrating database'
python3 manage.py migrate

echo 'Deploying django project on port 8000'
python3 manage.py runserver 0.0.0.0:8000