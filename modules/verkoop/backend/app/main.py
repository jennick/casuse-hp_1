# modules/verkoop/backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 👉 Import behoudt jouw bestaande structuur
from app.api.v1 import public, sellers, customers, customers_sync
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# --------------------------------------
# 🔹 CORS-configuratie — blijft behouden
# --------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------
# 🔹 Health & readiness endpoints
# --------------------------------------
@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict:
    return {"ready": True}


@app.get("/metrics")
def metrics() -> dict:
    return {"status": "metrics-not-implemented"}


# --------------------------------------
# 🔹 API v1 routers
# 👉 Alle routers correct geregistreerd
# --------------------------------------
app.include_router(public.router, prefix="/api/v1")
app.include_router(sellers.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(customers_sync.router, prefix="/api/v1")
