FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# ─────────────────────────────────────────────
# Systeem packages + cron
# ─────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    cron \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app

# ─────────────────────────────────────────────
# Python dependencies
# ─────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────
# Applicatiecode
# ─────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────
# Cron job: cleanup unfinished customers
# ─────────────────────────────────────────────
RUN touch /var/log/cron.log \
 && echo "*/15 * * * * python3 -m services.cleanup_customers >> /var/log/cron.log 2>&1" \
    > /etc/cron.d/cleanup-customers \
 && chmod 0644 /etc/cron.d/cleanup-customers \
 && crontab /etc/cron.d/cleanup-customers

# ─────────────────────────────────────────────
# Start: cron (foreground) + uvicorn
# ─────────────────────────────────────────────
CMD ["sh", "-c", "cron -f & uvicorn app:app --host 0.0.0.0 --port 8000"]
