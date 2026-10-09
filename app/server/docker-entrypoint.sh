#!/bin/sh
set -eu

echo "[entrypoint] Starting database migration"
python -m src.migrate_db
echo "[entrypoint] Database migration completed"

rm -rf /code/src/migrate_db.py /code/resources
echo "[entrypoint] Removed migration files"

echo "[entrypoint] Starting application: $*"
exec "$@"