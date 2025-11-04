import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import get_settings
from app.db import engine, SessionLocal
from app.api.v1 import auth, modules
from app.services.ai_agent import AIAgentService

settings = get_settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("casuse-hp-core")

app = FastAPI(title=settings.APP_NAME)
origins = [o.strip() for o in settings.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    logger.info("casuse-hp core-backend started on port %s", settings.APP_PORT)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

@app.middleware("http")
async def global_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("Unhandled error: %s", e)
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not-ready", "error": str(e)}

@app.post("/ai/ask")
def ai_ask(payload: dict):
    q = payload.get("question", "")
    svc = AIAgentService()
    return svc.answer(q)

app.include_router(auth.router)
app.include_router(modules.router)
