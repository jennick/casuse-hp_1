from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.db.session import get_session
from app.models.admin_user import AdminUser
from app.core.admin_auth import verify_password, create_access_token

router = APIRouter(
    prefix="/admin",
    tags=["admin-auth"],
)


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=AdminToken)
def admin_login(payload: AdminLoginRequest) -> AdminToken:
    """
    POST /api/v1/admin/login

    Body: { "email": "...", "password": "..." }

    Succes: { "access_token": "<jwt>", "token_type": "bearer" }
    Fout: 401 bij verkeerde login, 403 bij inactieve user.
    """
    db = get_session()
    try:
        user = (
            db.query(AdminUser)
            .filter(AdminUser.email == payload.email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User inactive",
            )

        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        token = create_access_token(user)
        return AdminToken(access_token=token)
    finally:
        db.close()
