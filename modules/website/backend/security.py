from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================================================
# Password helpers
# =====================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# =====================================================
# JWT helpers
# =====================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    COMMIT 2:
    - Deze functie ONDERSTEUNT nu ook 'customer_uuid'
    - Er wordt NIETS afgedwongen
    - Bestaande consumers blijven werken
    """
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.WEBSITE_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.WEBSITE_JWT_SECRET,
        algorithm=settings.WEBSITE_JWT_ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.

    COMMIT 2:
    - Geeft payload terug inclusief:
      - customer_id (intern, legacy)
      - customer_uuid (extern, nieuw)
    """
    payload = jwt.decode(
        token,
        settings.WEBSITE_JWT_SECRET,
        algorithms=[settings.WEBSITE_JWT_ALGORITHM],
    )
    return payload
