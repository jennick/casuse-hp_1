import logging
from typing import List, Dict, Any

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.customer import CustomerShadow

logger = logging.getLogger(__name__)


# -----------------------------------------------------
# Stap 1 — Klanten ophalen uit de website-module
# -----------------------------------------------------
async def fetch_customers_from_website() -> List[Dict[str, Any]]:
    url = f"{settings.WEBSITE_API_BASE_URL}/api/public/customers/"

    logger.info(f"Fetching customers FROM website: {url}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise RuntimeError(
            f"Website API returned {response.status_code}: {response.text}"
        )

    data = response.json()

    if "items" not in data:
        raise RuntimeError("Invalid website API response — expected key 'items'.")

    return data["items"]


# -----------------------------------------------------
# Stap 2 — Shadow customers in verkoop-db bijwerken
# -----------------------------------------------------
def sync_customers_into_verkoop(db: Session, customers: List[Dict[str, Any]]):
    created = 0
    updated = 0

    for c in customers:
        website_is_active = c.get("is_active", True)

        shadow = (
            db.query(CustomerShadow)
            .filter(CustomerShadow.website_customer_id == c["id"])
            .first()
        )

        if shadow is None:
            # --------- NIEUWE SHADOW ---------
            shadow = CustomerShadow(
                website_customer_id=c["id"],
                email=c["email"],
                first_name=c["first_name"],
                last_name=c["last_name"],
                phone_number=c.get("phone_number"),

                customer_type=c["customer_type"],
                description=c.get("description"),
                company_name=c.get("company_name"),
                tax_id=c.get("tax_id"),

                address_street=c.get("address_street"),
                address_ext_number=c.get("address_ext_number"),
                address_int_number=c.get("address_int_number"),
                address_neighborhood=c.get("address_neighborhood"),
                address_city=c.get("address_city"),
                address_state=c.get("address_state"),
                address_postal_code=c.get("address_postal_code"),
                address_country=c.get("address_country"),

                is_active=website_is_active,
                source="website-sync",
            )
            db.add(shadow)
            created += 1

        else:
            # --------- UPDATE BESTAANDE SHADOW ---------
            shadow.is_active = website_is_active

            shadow.email = c["email"]
            shadow.first_name = c["first_name"]
            shadow.last_name = c["last_name"]
            shadow.phone_number = c.get("phone_number")

            shadow.customer_type = c["customer_type"]
            shadow.description = c.get("description")
            shadow.company_name = c.get("company_name")
            shadow.tax_id = c.get("tax_id")

            shadow.address_street = c.get("address_street")
            shadow.address_ext_number = c.get("address_ext_number")
            shadow.address_int_number = c.get("address_int_number")
            shadow.address_neighborhood = c.get("address_neighborhood")
            shadow.address_city = c.get("address_city")
            shadow.address_state = c.get("address_state")
            shadow.address_postal_code = c.get("address_postal_code")
            shadow.address_country = c.get("address_country")

            updated += 1

    db.commit()

    return {
        "status": "ok",
        "created": created,
        "updated": updated,
        "total": created + updated,
    }
