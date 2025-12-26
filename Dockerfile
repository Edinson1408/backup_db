FROM python:3.11-slim

# -----------------------------
# Sistema + cron + clientes DB
# -----------------------------
RUN apt-get update && apt-get install -y \
    cron \
    default-mysql-client \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Directorio de trabajo
# -----------------------------
WORKDIR /app

# -----------------------------
# Dependencias Python
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Código
# -----------------------------
COPY . .

# -----------------------------
# Entrypoint con cron
# -----------------------------
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
