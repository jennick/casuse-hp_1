import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from initial_data import init_db

# ========================
# ROUTERS
# ========================

# Public (website-app)
from api.public.registration import router as public_register_router
from api.public.password_setup import router as public_password_setup_router
from api.public.login import router as public_login_router
from api.public.public_customers import router as public_customers_router

# Admin
from admin.auth import router as admin_auth_router
from admin.customers import router as admin_customers_router

# Extra admin modules
from audit.router import router as audit_router
from documents.router import router as documents_router
from relations.router import router as relations_router


logger = logging.getLogger("website-backend")

app = FastAPI(
    title="Casuse Website Backend",
    version="1.0.0",
)

# ========================
# CORS
# ========================

origins = [
    origin.strip()
    for origin in settings.WEBSITE_CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# REGISTER ROUTERS
# ========================

# Public
app.include_router(public_register_router)
app.include_router(public_password_setup_router)
app.include_router(public_login_router)
app.include_router(public_customers_router)

# Admin
app.include_router(admin_auth_router)
app.include_router(admin_customers_router)

# Extra admin modules
app.include_router(audit_router)
app.include_router(documents_router)
app.include_router(relations_router)

# ========================
# STARTUP
# ========================

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    init_db()
    logger.info("Website backend started, DB initialized.")

# ========================
# HEALTH
# ========================

@app.get("/health")
def health():
    return {"status": "ok"}
