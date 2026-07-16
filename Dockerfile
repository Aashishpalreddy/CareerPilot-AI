# ── CareerPilot AI backend (FastAPI) ─────────────────────────────────
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Runtime libs: libpq for psycopg, and common libs for lxml.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY alembic.ini ./
COPY docker/backend-entrypoint.sh ./docker/backend-entrypoint.sh
RUN chmod +x ./docker/backend-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker/backend-entrypoint.sh"]
