# website/backend/sales_sync.py

import logging
import os
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import settings
from crud import create_customer, get_customer_by_email
from deps import get_db
from models import Customer
from schemas import RegistrationRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["public-sales"])


class SalesAppCustomerCreate(BaseModel):
    """Payload die de verkopers-app naar de Website-backend stuurt.

    - seller_code: code van de verkoper in de verkoop-module (bv. S-0007)
    - registration: volledig registratie-object zoals /api/public/register
    """

    seller_code: str
    registration: RegistrationRequest


class SalesAppCustomerCreateResponse(BaseModel):
    success: bool
    website_customer_id: str
    already_existed: bool = False
    synced_to_sales: bool = False


def _get_verkoop_api_base_url() -> str:
    # Eerst proberen via Settings (mocht je het later toevoegen),
    # anders rechtstreeks uit de env met een veilig default.
    explicit = getattr(settings, "VERKOOP_API_BASE_URL", None)
    if explicit:
        return explicit

    return os.getenv("VERKOOP_API_BASE_URL", "http://host.docker.internal:20030")


def _get_verkoop_api_token() -> Optional[str]:
    explicit = getattr(settings, "VERKOOP_API_TOKEN", None)
    if explicit:
        return explicit
    return os.getenv("VERKOOP_API_TOKEN")


def sync_customer_to_sales(customer: Customer, seller_code: Optional[str]) -> bool:
    """Best-effort sync van een Website Customer naar de verkoop-module.

    - Maakt of updatet een CustomerShadow in de verkoop-module.
    - Koppelt optioneel aan een verkoper via seller_code.
    """

    base_url = _get_verkoop_api_base_url()
    if not base_url:
        logger.warning(
            "VERKOOP_API_BASE_URL niet geconfigureerd; skip sync voor customer %s",
            customer.id,
        )
        return False

    payload = {
        "website_customer_id": str(customer.id),
        "email": customer.email,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.phone_number,
        "customer_type": customer.customer_type.value
        if hasattr(customer, "customer_type")
        else "",
        "description": customer.description,
        "company_name": getattr(customer, "company_name", None),
        "tax_id": getattr(customer, "tax_id", None),
        "address_street": getattr(customer, "address_street", None),
        "address_ext_number": getattr(customer, "address_ext_number", None),
        "address_int_number": getattr(customer, "address_int_number", None),
        "address_neighborhood": getattr(customer, "address_neighborhood", None),
        "address_city": getattr(customer, "address_city", None),
        "address_state": getattr(customer, "address_state", None),
        "address_postal_code": getattr(customer, "address_postal_code", None),
        "address_country": getattr(customer, "address_country", None),
        "is_active": customer.is_active,
        "source": "sales_app",
        "seller_code": seller_code,
    }

    headers: dict[str, str] = {}
    token = _get_verkoop_api_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = httpx.post(
            f"{base_url.rstrip('/')}/api/v1/admin/customers/sync",
            json=payload,
            headers=headers,
            timeout=5.0,
        )
        resp.raise_for_status()
        return True
    except Exception as exc:  # pragma: no cover - netwerk
        logger.warning(
            "Sync naar verkoop-module mislukt voor customer %s: %s",
            customer.id,
            exc,
        )
        return False


@router.post(
    "/api/public/customers/from-sales-app",
    response_model=SalesAppCustomerCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def public_register_from_sales_app(
    payload: SalesAppCustomerCreate,
    db: Session = Depends(get_db),
) -> SalesAppCustomerCreateResponse:
    """Publiek endpoint voor de verkopers-app.

    Gedrag:
    - Als de klant (e-mail) al bestaat -> hergebruikt bestaande klant
    - Anders -> maakt nieuwe klant via bestaande create_customer-logica
    - Daarna -> best-effort sync naar verkoop-module
    """

    registration = payload.registration
    seller_code = payload.seller_code

    existing = get_customer_by_email(db, registration.email)
    already_existed = existing is not None

    if existing:
        customer = existing
    else:
        # Bestaande create_customer-functie gebruikt alle validatie
        # en mapping van RegistrationRequest naar Customer.
        customer = create_customer(
            db,
            registration=registration,
            hashed_password=None,
            is_admin=False,
        )

    synced = sync_customer_to_sales(customer, seller_code)

    return SalesAppCustomerCreateResponse(
        success=True,
        website_customer_id=str(customer.id),
        already_existed=already_existed,
        synced_to_sales=synced,
    )
