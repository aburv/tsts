#!/bin/sh
set -eu

echo "[entrypoint] Starting database migration"
if python -c "import src.migrate_db" 2>/dev/null; then
    python -m src.migrate_db
else
    echo "Migration module not found, skipping..."
fi
echo "[entrypoint] Database migration completed"

rm -rf /code/src/migrate_db.py /code/resources
echo "[entrypoint] Removed migration files"

echo "[entrypoint] Starting application: $*"
exec "$@"