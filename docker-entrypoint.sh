#!/bin/sh
set -e

# Valor por defecto si no existe en .env
: "${CRON_SCHEDULE:=0 3 * * *}"

echo "⏱️ CRON schedule: $CRON_SCHEDULE"

# Crear tarea cron
echo "$CRON_SCHEDULE /usr/local/bin/python3 /app/main.py >> /var/log/db_backup.log 2>&1" > /etc/cron.d/db-backup

chmod 0644 /etc/cron.d/db-backup
crontab /etc/cron.d/db-backup

# Ejecutar una vez al iniciar (opcional pero recomendado)
/usr/local/bin/python3 /app/main.py

# Mantener cron en foreground
cron -f
