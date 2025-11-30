FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialise database schema and demo data, then start API
CMD ["bash", "-lc", "python -m app.scripts.init_db && uvicorn app.main:app --host 0.0.0.0 --port 20030"]
