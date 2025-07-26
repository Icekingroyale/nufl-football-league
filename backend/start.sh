#!/bin/bash
# Production startup script for Render

echo "Starting NUFL Football League Backend..."

# Set environment variables
export FLASK_APP=wsgi.py
export FLASK_ENV=production

# Start Gunicorn with proper configuration
exec gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 