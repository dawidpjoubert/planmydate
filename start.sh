#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn ldg.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 5