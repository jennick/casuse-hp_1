import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_db
from schemas import RegistrationRequest
from crud import get_customer_by_email, create_customer
from services.registration_tokens import create_registration_token
from services.email import send_registration_email
from config import settings

router = APIRouter(
    prefix="/api/public",
    tags=["Public Registration"],
)

logger = logging.getLogger(__name__)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def public_register(
    registration: RegistrationRequest,
    db: Session = Depends(get_db),
):
    # -------------------------------------------------
    # 1. Check of e-mail al bestaat
    # -------------------------------------------------
    existing = get_customer_by_email(db, registration.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # -------------------------------------------------
    # 2. Customer aanmaken (bron van waarheid)
    # -------------------------------------------------
    customer = create_customer(db, registration=registration)

    # -------------------------------------------------
    # 3. Registratie / password-setup token aanmaken
    # -------------------------------------------------
    token = create_registration_token(db, customer)

    # -------------------------------------------------
    # 4. Registratie e-mail versturen (BEST EFFORT)
    #    → mag NOOIT de registratie breken
    # -------------------------------------------------
    try:
        send_registration_email(
            customer=customer,
            token=token,
        )
        email_sent = True
    except Exception:
        email_sent = False
        logger.exception(
            "Registratie succesvol, maar e-mail verzenden mislukt voor %s",
            customer.email,
        )

    # -------------------------------------------------
    # 5. Logging (diagnostisch, veilig voor prod)
    # -------------------------------------------------
    base_url = settings.WEBSITE_PUBLIC_BASE_URL.rstrip("/")
    setup_url = f"{base_url}/password-setup?token={token.token}"

    if email_sent:
        logger.info(
            "Registration completed for %s — password setup URL sent",
            customer.email,
        )
    else:
        logger.warning(
            "Registration completed for %s — password setup URL NOT sent (%s)",
            customer.email,
            setup_url,
        )

    # -------------------------------------------------
    # 6. API response (registratie = OK)
    # -------------------------------------------------
    return {
        "status": "ok",
    }
