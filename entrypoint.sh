#!/bin/bash
set -e

# ✅ Load .env variables safely
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# ✅ Wait for PostgreSQL to be ready
echo "Waiting for database..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Database is ready."

# ✅ Ensure the database exists before migrations
python create_db.py

# ✅ Apply migrations
echo "Applying database migrations..."
alembic upgrade head

# ✅ Start the app
exec "$@"
