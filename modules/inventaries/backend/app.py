import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

MODULE_NAME = os.getenv("MODULE_NAME", "inventaries")
MODULE_PORT = int(os.getenv("MODULE_PORT", 20070))
ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(title=f"casuse-hp - Inventaris backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "module": MODULE_NAME}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "module": MODULE_NAME}

@app.get("/info")
def info():
    return {
        "module": MODULE_NAME,
        "port": MODULE_PORT,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=MODULE_PORT)
