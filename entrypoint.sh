#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for database..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "Database is ready."

# Run database creation script
python create_db.py

# Run Alembic migrations
alembic upgrade head

# Start the app (modify this based on your app)
exec "$@"
