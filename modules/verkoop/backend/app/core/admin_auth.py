import os
from datetime import datetime, timedelta
from typing import Any, Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_engine, get_session  # jouw eigen helpers
from app.models.admin_user import AdminUser

# ---------------------------------------------------------
# Config uit environment
# ---------------------------------------------------------

VERKOOP_JWT_SECRET = os.getenv("VERKOOP_JWT_SECRET", "dev-verkoop-secret-change-me")
VERKOOP_JWT_EXP_SECONDS = int(os.getenv("VERKOOP_JWT_EXP_SECONDS", "86400"))
JWT_ALGORITHM = "HS256"

security_scheme = HTTPBearer(auto_error=False)


# ---------------------------------------------------------
# Password hashing helpers
# ---------------------------------------------------------


def hash_password(plain: str) -> str:
    """
    Hash een plain tekst wachtwoord met bcrypt.
    """
    if not plain:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifieer een plain password tegen een bcrypt hash.
    """
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        # Als de hash corrupt is of een vreemd formaat heeft
        return False


# ---------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------


def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    """
    Maak een JWT access token voor een gegeven subject (meestal user_id).
    """
    if expires_delta is None:
        expires_delta = timedelta(seconds=VERKOOP_JWT_EXP_SECONDS)

    now = datetime.utcnow()
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + expires_delta,
    }
    token = jwt.encode(payload, VERKOOP_JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """
    Decodeer een JWT en geef de payload terug.
    Gooit HTTP 401 bij fouten.
    """
    try:
        payload = jwt.decode(token, VERKOOP_JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# ---------------------------------------------------------
# Dependency: huidige admin user
# ---------------------------------------------------------


def _get_db_session() -> Session:
    """
    Gebruik jouw bestaande session-logica:
    - get_engine() initialiseert de engine / SessionLocal
    - get_session() geeft een Session-instance terug
    """
    # Zorg dat engine/SessionLocal zeker geïnitialiseerd is
    get_engine()
    return get_session()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> AdminUser:
    """
    Haalt de huidige ingelogde AdminUser op o.b.v. de Bearer token.

    Wordt gebruikt als dependency in routes, bijv:
        current_admin: AdminUser = Depends(get_current_admin)
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials
    payload = decode_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        )

    db = _get_db_session()
    try:
        user = db.get(AdminUser, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )
        return user
    finally:
        db.close()
