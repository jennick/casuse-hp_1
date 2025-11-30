from datetime import datetime, timedelta
from secrets import token_hex
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session

from app.core.security import require_scope
from app.core.seller_auth import hash_seller_password
from app.db.session import get_session
from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerUpdate, SellerOut
from app.services.email_service import EmailService  # voor toekomstige mailflow


router = APIRouter(prefix="/sellers", tags=["sellers"])


def _generate_internal_number(db: Session) -> str:
    """
    Genereer een random, uniek intern nummer dat niet zichtbaar is voor klanten.
    """
    for _ in range(32):
        candidate = token_hex(4)  # 8 hex-karakters
        exists = (
            db.query(Seller)
            .filter(Seller.phone_internal == candidate)
            .first()
        )
        if not exists:
            return candidate

    raise RuntimeError("Kon geen uniek intern nummer genereren")


# =========================
# Basis CRUD
# =========================

@router.get("", response_model=List[SellerOut])
def list_sellers(
    request: Request,
    db: Session = Depends(get_session),
) -> List[SellerOut]:
    _ = require_scope(request, "verkoop:read")
    sellers = (
        db.query(Seller)
        .order_by(Seller.seller_code.asc())
        .all()
    )
    return sellers


@router.post(
    "",
    response_model=SellerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_seller(
    payload: SellerCreate,
    request: Request,
    db: Session = Depends(get_session),
) -> SellerOut:
    _ = require_scope(request, "verkoop:admin")

    data = payload.model_dump()

    if not data.get("phone_internal"):
        data["phone_internal"] = _generate_internal_number(db)

    seller = Seller(**data)
    db.add(seller)
    db.commit()
    db.refresh(seller)

    if not seller.seller_code:
        seller.seller_code = f"S-{seller.id:04d}"
        db.add(seller)
        db.commit()
        db.refresh(seller)

    return seller


@router.get(
    "/{seller_id}",
    response_model=SellerOut,
)
def get_seller(
    seller_id: int,
    request: Request,
    db: Session = Depends(get_session),
) -> SellerOut:
    _ = require_scope(request, "verkoop:read")

    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )
    return seller


@router.patch(
    "/{seller_id}",
    response_model=SellerOut,
)
def update_seller(
    seller_id: int,
    payload: SellerUpdate,
    request: Request,
    db: Session = Depends(get_session),
) -> SellerOut:
    _ = require_scope(request, "verkoop:admin")

    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )

    data = payload.model_dump(exclude_unset=True)

    if "phone_internal" not in data:
        data.pop("phone_internal", None)

    for field, value in data.items():
        setattr(seller, field, value)

    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


@router.delete(
    "/{seller_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_seller(
    seller_id: int,
    request: Request,
    db: Session = Depends(get_session),
) -> None:
    _ = require_scope(request, "verkoop:admin")

    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )

    db.delete(seller)
    db.commit()


# =========================
# Password reset (admin + publiek)
# =========================

class SellerResetPasswordPayload(BaseModel):
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)


@router.post(
    "/{seller_id}/password-reset-request",
    status_code=status.HTTP_200_OK,
)
def create_password_reset_request(
    seller_id: int,
    request: Request,
    db: Session = Depends(get_session),
) -> dict:
    """
    Admin: maak een resetlink voor een verkoper.
    """
    _ = require_scope(request, "verkoop:admin")

    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )

    token = token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)

    seller.reset_token = token
    seller.reset_token_expires_at = expires_at
    db.add(seller)
    db.commit()
    db.refresh(seller)

    origin = request.headers.get("origin") or request.headers.get("Origin")
    if not origin:
        origin = "http://localhost:20040"
    origin = origin.rstrip("/")

    reset_url = f"{origin}/reset-password?token={token}"

    return {
        "reset_url": reset_url,
        "valid_until": expires_at.isoformat() + "Z",
    }


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
)
def seller_reset_password(
    payload: SellerResetPasswordPayload,
    db: Session = Depends(get_session),
) -> dict:
    """
    Publiek endpoint: stel een nieuw wachtwoord in op basis van een token.
    """

    # 1. Zoeken op token (zonder datetime-vergelijking in de query)
    seller = (
        db.query(Seller)
        .filter(Seller.reset_token == payload.token)
        .first()
    )

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    expires_at = seller.reset_token_expires_at

    # 2. Check verlopen / ontbrekend, robuust voor tz / geen tz
    if not expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    # normaliseer 'nu' naar dezelfde tz als expires_at (of geen tz)
    if expires_at.tzinfo is None:
        now = datetime.utcnow()
    else:
        now = datetime.now(tz=expires_at.tzinfo)

    if expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    # 3. Wachtwoord hashen en opslaan
    try:
        seller.password_hash = hash_seller_password(payload.new_password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kan wachtwoord momenteel niet instellen.",
        )

    # 4. Token ongeldig maken
    seller.reset_token = None
    seller.reset_token_expires_at = None

    db.add(seller)
    db.commit()

    return {"status": "ok"}


# =========================
# Password reset via e-mail (voor verkopers-app, toekomstig gebruik)
# =========================

class SellerPasswordResetRequestEmail(BaseModel):
    email: EmailStr


@router.post(
    "/password-reset-request-email",
    status_code=status.HTTP_200_OK,
)
def seller_request_password_reset_email(
    payload: SellerPasswordResetRequestEmail,
    request: Request,
    db: Session = Depends(get_session),
) -> dict:
    """
    Endpoint voor verkopers-app (toekomstig gebruik):

    - Ontvangt enkel een e-mailadres.
    - Als de verkoper bestaat:
      * Genereert een reset_token + expiry
      * Bouwt een reset-link
      * Roept EmailService aan (in dev: logt enkel)
    - Retourneert ALTIJD 200 {"status": "ok"} om niet te lekken
      of een e-mailadres al dan niet bestaat.
    """

    seller = (
        db.query(Seller)
        .filter(Seller.email_work == payload.email)
        .first()
    )

    if seller:
        token = token_hex(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)

        seller.reset_token = token
        seller.reset_token_expires_at = expires_at
        db.add(seller)
        db.commit()
        db.refresh(seller)

        origin = request.headers.get("origin") or request.headers.get("Origin")
        if not origin:
            origin = "http://localhost:20040"
        origin = origin.rstrip("/")

        reset_url = f"{origin}/reset-password?token={token}"

        # In dev: logt enkel; in prod: stuurt echte mail als SMTP is geconfigureerd
        EmailService.send_password_reset_email(
            to_email=seller.email_work,
            reset_link=reset_url,
        )

    return {"status": "ok"}
