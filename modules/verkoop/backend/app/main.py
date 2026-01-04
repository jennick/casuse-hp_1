from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.sellers import router as sellers_router
from app.api.v1.customers import router as customers_router
from app.api.v1.customers_sync import router as customers_sync_router
from app.core.config import settings


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": True}

# API v1
app.include_router(sellers_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(customers_sync_router, prefix="/api/v1")
