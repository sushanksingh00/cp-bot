#!/bin/sh

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running migrations..."
    alembic upgrade head
fi

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}