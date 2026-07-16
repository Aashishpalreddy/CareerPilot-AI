#!/usr/bin/env sh
set -e

echo "Waiting for database at ${DB_HOST}:${DB_PORT} ..."
python - <<'PY'
import os, time, socket
host = os.environ.get("DB_HOST", "localhost")
port = int(os.environ.get("DB_PORT", "5432"))
for attempt in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Database is reachable.")
            break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit(f"Database at {host}:{port} not reachable after 60s")
PY

echo "Running Alembic migrations ..."
alembic upgrade head

echo "Starting API server ..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
