
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pythonjsonlogger import jsonlogger
import logging, time, uuid, os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from app.core.config import settings
from app.api.v1 import (
    sellers,
    assignments,
    quotes,
    orders,
    payments,
    public,
    ai,
    admin,
    number_series,
)

logger = logging.getLogger("uvicorn")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("%(levelname)s %(asctime)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)

REQUESTS = Counter("http_requests_total","Total HTTP Requests",["path","method","status"])

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        start = time.time()
        response: Response = await call_next(request)
        duration = round((time.time()-start)*1000,2)
        logger.info({"cid": cid, "path": request.url.path, "status": response.status_code, "ms": duration})
        REQUESTS.labels(path=request.url.path, method=request.method, status=response.status_code).inc()
        response.headers["X-Correlation-ID"] = cid
        return response

app = FastAPI(title="Casuse Verkoop", version="1.0.0")
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/readyz")
def readyz():
    return {"ready": True}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(sellers.router, prefix="/api/v1")
app.include_router(number_series.router, prefix="/api/v1")
app.include_router(quotes.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(assignments.router, prefix="/api/v1")
app.include_router(public.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(number_series.router, prefix="/api/v1")