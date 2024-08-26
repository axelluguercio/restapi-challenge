#!/bin/bash

# Migrations
echo "Applying database migrations..."
flask db upgrade

# start app
echo "Starting the application..."
exec gunicorn -b 0.0.0.0:3000  --access-logfile - --graceful-timeout 30 --timeout 30 run:app