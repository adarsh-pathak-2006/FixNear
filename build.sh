#!/usr/bin/env bash
# build.sh — Render build script.
# Render calls this script once during every deploy before starting the server.
# Set the "Build Command" in Render to:  ./build.sh
# Set the "Start Command" in Render to:  gunicorn fixnear.wsgi:application

set -o errexit  # Exit immediately if any command fails.

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
