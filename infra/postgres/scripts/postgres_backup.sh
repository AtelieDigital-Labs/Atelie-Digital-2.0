#!/bin/sh

set -e

BACKUP_DIR="/backups"

mkdir -p "$BACKUP_DIR"

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

docker exec postgres \
    pg_dump \
    -U "$DATABASE_USER" \
    -d "$DATABASE_DB" \
    -Fc \
    > "$BACKUP_DIR/postgres-$DATE.dump"

# Mantém apenas 7 dias
find "$BACKUP_DIR" -name "*.dump" -mtime +7 -delete

echo "Backup realizado: postgres-$DATE.dump"
