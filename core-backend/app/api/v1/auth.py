from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pyotp
from jose import jwt, JWTError
from app.db import get_db
from app.models.user import User
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

class LoginRequest(BaseModel):
    username: str
    password: str
    totp: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    twofa_enabled: bool

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if settings.ENABLE_2FA and user.twofa_enabled:
        if not data.totp:
            raise HTTPException(status_code=400, detail="TOTP code required")
        if not user.twofa_secret:
            raise HTTPException(status_code=400, detail="No 2FA secret for user")
        totp = pyotp.TOTP(user.twofa_secret)
        if not totp.verify(data.totp, valid_window=1):
            raise HTTPException(status_code=400, detail="Invalid TOTP code")
    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role}, access_expires)
    refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email, "role": user.role}, refresh_expires)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access_token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=MeResponse)
def me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return MeResponse(id=user.id, email=user.email, role=user.role, is_active=user.is_active, twofa_enabled=user.twofa_enabled)

class TwoFASetupResponse(BaseModel):
    secret: str
    otpauth_url: str

@router.post("/2fa/setup", response_model=TwoFASetupResponse)
def setup_2fa(db: Session = Depends(get_db)):
    if not settings.ENABLE_2FA:
        raise HTTPException(status_code=400, detail="2FA disabled")
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user")
    secret = pyotp.random_base32()
    user.twofa_secret = secret
    db.add(user)
    db.commit()
    otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="casuse-hp")
    return TwoFASetupResponse(secret=secret, otpauth_url=otpauth_url)

class TwoFAVerifyRequest(BaseModel):
    code: str

@router.post("/2fa/verify")
def verify_2fa(data: TwoFAVerifyRequest, db: Session = Depends(get_db)):
    if not settings.ENABLE_2FA:
        raise HTTPException(status_code=400, detail="2FA disabled")
    user = db.query(User).first()
    if not user or not user.twofa_secret:
        raise HTTPException(status_code=404, detail="No user/secret")
    totp = pyotp.TOTP(user.twofa_secret)
    if not totp.verify(data.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid code")
    user.twofa_enabled = True
    db.add(user)
    db.commit()
    return {"status": "2FA verified"}
