import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from models import RegistrationToken, Customer
from config import settings


def create_registration_token(db: Session, customer: Customer) -> RegistrationToken:
    """
    Maakt een eenmalig registratie-/reset-token aan voor een klant.
    Wordt gebruikt voor:
    - initiële registratie
    - admin password reset
    """

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.REGISTRATION_TOKEN_EXPIRE_MINUTES
    )

    token = RegistrationToken(
        token=str(uuid.uuid4()),
        customer_id=customer.id,
        expires_at=expires_at,
        used=False,
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token
