from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.orm import Session

from database import SessionLocal
from security import decode_access_token
from schemas import TokenData
from crud import get_customer_by_email
from models import Customer


# =========================================================
# OAuth2 scheme
# =========================================================
# ⚠️ Dit tokenUrl is ENKEL relevant voor OpenAPI / Swagger.
# De effectieve login voor admin gebeurt via /api/admin/login
# Klant-login wordt later apart behandeld.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/admin/login"
)


# =========================================================
# Database dependency
# =========================================================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# Current user (GENERIC)
# =========================================================
# ⚠️ BELANGRIJK:
# - Hier GEEN is_active check
# - Deze dependency wordt gebruikt door:
#   - admin routes
#   - interne routes
# - Statuscontrole gebeurt contextueel (bv. admin vs public)
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Customer:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(
            email=email,
            customer_id=payload.get("customer_id"),
            is_admin=payload.get("is_admin"),
        )

    except JWTError:
        raise credentials_exception

    user = get_customer_by_email(db, token_data.email)

    # ❗ GEEN is_active check hier
    if user is None:
        raise credentials_exception

    return user


# =========================================================
# Current admin user
# =========================================================
# - Enkel admins toegelaten
# - Wordt gebruikt door /api/admin/*
# =========================================================

def get_current_admin_user(
    current_user: Customer = Depends(get_current_user),
) -> Customer:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user
