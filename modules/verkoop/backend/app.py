import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1 import public, sellers, customers

MODULE_NAME = os.getenv("MODULE_NAME", "verkoop")
MODULE_PORT = int(os.getenv("MODULE_PORT", 20030))
ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(title="casuse-hp - Verkoop backend")

# CORS-configuratie zoals vroeger
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    """Health endpoint – behoudt oude response-structuur."""
    return {"status": "ok", "module": MODULE_NAME}


@app.get("/readyz")
def readyz():
    """Readiness endpoint – idem als vroeger."""
    return {"status": "ready", "module": MODULE_NAME}


@app.get("/metrics")
def metrics():
    """Placeholder voor metrics-endpoint."""
    return {"status": "metrics-not-implemented", "module": MODULE_NAME}


@app.get("/info")
def info():
    """Basis-informatie over deze module."""
    return {
        "module": MODULE_NAME,
        "port": MODULE_PORT,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


# API v1 routers – HIER komen sellers, public en customers binnen
app.include_router(sellers.router, prefix="/api/v1")
app.include_router(public.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=MODULE_PORT)
