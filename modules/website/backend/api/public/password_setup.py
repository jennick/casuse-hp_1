import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_db
from schemas import (
    PasswordSetupTokenInfo,
    PasswordSetupRequest,
    PasswordSetupResponse,
)
from crud import (
    get_registration_token,
    mark_registration_token_used,
    set_customer_password,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/public",
    tags=["Public Password Setup"],
)

# ============================================================
# VALIDATE TOKEN
# ============================================================

@router.get(
    "/password-setup/{token}",
    response_model=PasswordSetupTokenInfo,
    summary="Validate password setup token",
)
def validate_password_setup_token(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Valideert of een password-setup token:
    - bestaat
    - niet gebruikt is
    - niet verlopen is
    """

    token_obj = get_registration_token(db, token)

    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired token",
        )

    if token_obj.used:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token already used",
        )

    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token expired",
        )

    return PasswordSetupTokenInfo.from_orm(token_obj)


# ============================================================
# SET PASSWORD
# ============================================================

@router.post(
    "/password-setup/{token}",
    response_model=PasswordSetupResponse,
    summary="Set password using registration token",
)
def set_password_from_token(
    token: str,
    payload: PasswordSetupRequest,
    db: Session = Depends(get_db),
):
    """
    Zet het wachtwoord voor een klant via een geldig token.
    - activeert de klant
    - markeert token als gebruikt
    """

    token_obj = get_registration_token(db, token)

    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired token",
        )

    if token_obj.used:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token already used",
        )

    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token expired",
        )

    customer = token_obj.customer

    # Zet wachtwoord
    set_customer_password(db, customer, payload.password)

    # Activeer klant
    customer.is_active = True
    customer.updated_at = datetime.now(timezone.utc)

    # Token markeren als gebruikt
    mark_registration_token_used(db, token_obj)

    logger.info(
        "Password setup completed for customer %s",
        customer.email,
    )

    return PasswordSetupResponse(success=True)
