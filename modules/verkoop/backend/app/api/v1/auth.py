from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginIn, TokenOut, MeOut
from app.core.admin_auth import verify_password, create_access_token, get_current_admin
from app.models.admin_user import AdminUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(subject=user.email, user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=MeOut)
def read_me(current: AdminUser = Depends(get_current_admin)):
    return {
        "id": current.id,
        "email": current.email,
        "full_name": current.full_name,
    }
