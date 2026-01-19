#!/bin/bash
# Production startup script for Render
cd "$(dirname "$0")"
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 wsgi:app

