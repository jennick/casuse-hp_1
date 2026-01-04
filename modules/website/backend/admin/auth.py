from datetime import timedelta
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_db
from security import (
    verify_password,
    create_access_token,
)
from models import Customer
from schemas import LoginRequest, Token
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Auth"],
)

# =========================================================
# ADMIN LOGIN
# =========================================================

@router.post("/login", response_model=Token)
def admin_login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Admin login:
    - Enkel klanten met is_admin = True
    - Vereist wachtwoord
    """

    user: Customer | None = (
        db.query(Customer)
        .filter(Customer.email == payload.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an admin account",
        )

    if not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not set",
        )

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    access_token_expires = timedelta(
        minutes=settings.WEBSITE_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "customer_id": str(user.id),
            "is_admin": True,
        },
        expires_delta=access_token_expires,
    )

    logger.info("Admin login successful: %s", user.email)

    return Token(access_token=access_token)
