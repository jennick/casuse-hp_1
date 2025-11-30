# verkoop/backend/app/api/v1/customers_sync.py

import logging
from typing import Any, List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session
from app.models.customer import CustomerShadow
from app.schemas.customer import CustomerShadowOut

logger = logging.getLogger(__name__)

# main.py include't deze router met prefix=settings.API_V1_STR ("/api/v1")
# => volledige URL's:
#    GET  /api/v1/customers/sync-from-website
#    POST /api/v1/customers/sync-from-website
router = APIRouter(
    prefix="/customers",
    tags=["customers-sync"],
)


async def _try_get_website_admin_token(
    client: httpx.AsyncClient,
) -> Optional[str]:
    """
    Probeer in te loggen op de Website-backend als admin.

    - Als WEBSITE_ADMIN_EMAIL/WEBSITE_ADMIN_PASSWORD niet gezet zijn:
        -> return None (geen token, we proberen zonder auth).
    - Als login-endpoint 404 geeft:
        -> log een waarschuwing en return None (geen crash).
    - Als login-endpoint 401/403 geeft:
        -> raise HTTPException met duidelijke fout (credentials fout).
    - Bij 200 met access_token:
        -> return token.
    """

    email = settings.WEBSITE_ADMIN_EMAIL
    password = settings.WEBSITE_ADMIN_PASSWORD

    if not email or not password:
        logger.info(
            "Geen WEBSITE_ADMIN_EMAIL/WEBSITE_ADMIN_PASSWORD ingesteld; "
            "probeer Website-adminendpoint zonder auth."
        )
        return None

    base_url = settings.WEBSITE_API_BASE_URL.rstrip("/")
    # LET OP: op de website-backend bestaat /api/public/login (zonder /v1)
    login_url = f"{base_url}/api/public/login"

    logger.info("Probeer Website-adminlogin op: %s (user=%s)", login_url, email)

    try:
        resp = await client.post(
            login_url,
            json={"email": email, "password": password},
            timeout=15.0,
        )
    except httpx.RequestError as exc:
        logger.error("Website-login endpoint niet bereikbaar: %s", exc)
        # we vallen terug op 'geen token' zodat we verder kunnen proberen
        return None

    if resp.status_code == 404:
        logger.warning(
            "Website-login endpoint %s bestaat niet (404). "
            "Ga verder zonder admin-token.",
            login_url,
        )
        return None

    if resp.status_code in (401, 403):
        logger.error(
            "Website-login weigert credentials (status=%s): %s",
            resp.status_code,
            resp.text,
        )
        raise HTTPException(
            status_code=502,
            detail=(
                "Website-adminlogin mislukt (401/403). "
                "Controleer WEBSITE_ADMIN_EMAIL en WEBSITE_ADMIN_PASSWORD."
            ),
        )

    if resp.status_code != 200:
        logger.error(
            "Website-login gaf onverwachte status %s: %s",
            resp.status_code,
            resp.text,
        )
        # in dev: ga verder zonder token, misschien is admin/customers toch publiek
        return None

    data = resp.json()
    token = data.get("access_token")
    if not token:
        logger.warning(
            "Website-login antwoordde zonder access_token: %r. "
            "Ga verder zonder admin-token.",
            data,
        )
        return None

    return token


async def _sync_from_website_impl(db: Session) -> List[CustomerShadowOut]:
    """
    Interne implementatie van de sync.

    Deze functie:
    - Haalt klanten op uit de Website-backend (admin-lijst).
    - Schrijft/updatet CustomerShadow records in de verkoop-database.
    - Geeft de gesynchroniseerde lijst CustomerShadowOut terug.
    """

    base_url = settings.WEBSITE_API_BASE_URL.rstrip("/")
    # BELANGRIJK: Website-backend heeft /api/admin/customers (zonder /v1)
    customers_url = f"{base_url}/api/admin/customers"

    logger.info("Start synchronisatie klanten vanuit Website: %s", customers_url)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1) Optioneel: admin-token ophalen
        headers = {}
        token = await _try_get_website_admin_token(client)
        if token:
            headers["Authorization"] = f"Bearer {token}"

        # 2) Admin/customers endpoint aanroepen
        try:
            resp = await client.get(customers_url, headers=headers)
        except httpx.RequestError as exc:
            logger.error("Website-API niet bereikbaar: %s", exc)
            raise HTTPException(
                status_code=502,
                detail=f"Website-API niet bereikbaar: {exc!s}",
            )

    if resp.status_code == 401:
        logger.error("Website-API antwoordde 401 (unauthorized): %s", resp.text)
        raise HTTPException(
            status_code=502,
            detail=(
                "Website-API weigert toegang (401). "
                "Waarschijnlijk is het adminendpoint beschermd. "
                "Configureer een geldig login-endpoint of maak /api/admin/customers "
                "intern toegankelijk voor de verkoop-backend."
            ),
        )

    if resp.status_code != 200:
        logger.error(
            "Website-API gaf status %s terug: %s",
            resp.status_code,
            resp.text,
        )
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Website-API gaf status {resp.status_code} terug",
        )

    data: Any = resp.json()

    # Admin endpoint retourneert CustomersListResponse:
    #   { "items": [...], "total": <int> }
    if isinstance(data, dict):
        customers = data.get("items", [])
    elif isinstance(data, list):
        customers = data
    else:
        logger.error("Onverwacht response-formaat van Website-API: %r", data)
        raise HTTPException(
            status_code=502,
            detail="Onverwacht response-formaat van Website-API",
        )

    if not isinstance(customers, list):
        logger.error(
            "Field 'items' is geen lijst in Website-API response: %r",
            customers,
        )
        raise HTTPException(
            status_code=502,
            detail="Website-API retourneerde een ongeldig 'items'-veld",
        )

    # --- Upsert naar CustomerShadow -----------------------------------------
    result: List[CustomerShadowOut] = []

    for item in customers:
        if not isinstance(item, dict):
            # safety: vreemde records overslaan
            continue

        website_customer_id = item.get("id")
        email = item.get("email")

        if website_customer_id is None or email is None:
            # Zonder id / email kunnen we niet betrouwbaar syncen
            continue

        website_customer_id = str(website_customer_id)

        # Eerst proberen op website_customer_id (unieke sleutel)
        shadow: Optional[CustomerShadow] = (
            db.query(CustomerShadow)
            .filter(CustomerShadow.website_customer_id == website_customer_id)
            .first()
        )

        # Fallback op e-mail (oude records of gewijzigde id's)
        if shadow is None:
            shadow = (
                db.query(CustomerShadow)
                .filter(CustomerShadow.email == email)
                .first()
            )

        # Nog niets gevonden? Nieuwe shadow aanmaken.
        if shadow is None:
            shadow = CustomerShadow(
                website_customer_id=website_customer_id,
                email=email,
            )
            db.add(shadow)

        # Velden defensief mappen
        shadow.email = email or shadow.email

        first_name = item.get("first_name")
        if first_name:
            shadow.first_name = first_name

        last_name = item.get("last_name")
        if last_name:
            shadow.last_name = last_name

        customer_type = item.get("customer_type")
        if customer_type is not None:
            shadow.customer_type = str(customer_type)

        company_name = item.get("company_name")
        if company_name:
            shadow.company_name = company_name

        phone_number = (
            item.get("phone_number")
            or item.get("phone")
            or item.get("gsm")
        )
        if phone_number:
            shadow.phone_number = phone_number

        # Adres velden, indien aanwezig in de website-respons
        for field in [
            "address_street",
            "address_ext_number",
            "address_int_number",
            "address_neighborhood",
            "address_city",
            "address_state",
            "address_postal_code",
            "address_country",
        ]:
            value = item.get(field)
            if value:
                setattr(shadow, field, value)

        # Status-actief overnemen indien meegegeven
        if "is_active" in item:
            shadow.is_active = bool(item["is_active"])

        # Bron aanduiden; overschrijf enkel als er nog niets stond
        if shadow.source is None:
            shadow.source = "website_admin_sync"

        db.flush()

        # Pydantic v2: from_attributes=True i.p.v. orm_mode
        result.append(
            CustomerShadowOut.model_validate(
                shadow,
                from_attributes=True,
            )
        )

    db.commit()
    logger.info("Synchronisatie voltooid, %s klanten verwerkt", len(result))

    return result


# ---------- Publieke endpoints (GET, POST en OPTIONS) -----------------------


@router.options("/sync-from-website")
async def sync_from_website_options() -> Response:
    """Handmatige OPTIONS-handler voor eventuele preflight-requests."""
    return Response(status_code=200)


@router.get(
    "/sync-from-website",
    response_model=List[CustomerShadowOut],
)
async def sync_from_website_get(
    db: Session = Depends(get_session),
) -> List[CustomerShadowOut]:
    """GET-variant voor de frontend-knop (en voor testen in de browser)."""
    return await _sync_from_website_impl(db)


@router.post(
    "/sync-from-website",
    response_model=List[CustomerShadowOut],
)
async def sync_from_website_post(
    db: Session = Depends(get_session),
) -> List[CustomerShadowOut]:
    """POST-variant (bruikbaar in scripts, tools of toekomstige flows)."""
    return await _sync_from_website_impl(db)
