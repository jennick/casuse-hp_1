from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from deps import get_db
from schemas import LoginRequest, Token
from crud import get_customer_by_email
from security import verify_password, create_access_token
from config import settings

router = APIRouter(
    prefix="/api/public",
    tags=["Public Login"],
)


@router.post("/login", response_model=Token)
def public_login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = get_customer_by_email(db, login_data.email)

    if not user or not user.hashed_password:
        raise HTTPException(401, "Incorrect email or password")

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password")

    if not user.is_active:
        raise HTTPException(400, "User is inactive")

    access_token = create_access_token(
        data={
            "sub": user.email,

            # ⚠️ legacy intern ID (nog behouden voor backward compatibility)
            "customer_id": str(user.id),

            # 🔐 extern, stabiel klant-ID (COMMIT 2)
            "customer_uuid": str(user.customer_uuid),

            "scope": "customer",
        },
        expires_delta=timedelta(
            minutes=settings.WEBSITE_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return Token(access_token=access_token)
