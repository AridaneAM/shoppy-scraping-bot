#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.5
done
echo "Init telegram bot"

exec sudo python3 -u app.py