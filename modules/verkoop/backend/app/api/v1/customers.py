# verkoop/backend/app/api/v1/customers.py

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.security import require_scope
from app.db.session import get_session
from app.models.customer import CustomerShadow, CustomerSellerAssignment
from app.models.domain_event import DomainEvent
from app.models.seller import Seller
from app.schemas.customer import (
    CustomerAssignmentHistoryItem,
    CustomerAssignmentRequest,
    CustomerListItem,
    CustomerListResponse,
    CustomerShadowOut,
    CustomerSyncPayload,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/customers", tags=["customers"])


def _get_active_assignment(
    db: Session, customer_id: int
) -> Optional[CustomerSellerAssignment]:
    return (
        db.query(CustomerSellerAssignment)
        .filter(
            CustomerSellerAssignment.customer_id == customer_id,
            CustomerSellerAssignment.unassigned_at.is_(None),
        )
        .order_by(CustomerSellerAssignment.assigned_at.desc())
        .first()
    )


def _build_customer_shadow_out(
    db: Session, shadow: CustomerShadow
) -> CustomerShadowOut:
    assignment = _get_active_assignment(db, shadow.id)
    current_seller_id: Optional[int] = None
    current_seller_code: Optional[str] = None
    current_seller_name: Optional[str] = None

    if assignment is not None:
        seller = db.query(Seller).get(assignment.seller_id)
        if seller is not None:
            current_seller_id = seller.id
            current_seller_code = seller.seller_code
            full_name_parts = [seller.first_name, seller.last_name]
            current_seller_name = " ".join(p for p in full_name_parts if p)

    return CustomerShadowOut(
        id=shadow.id,
        website_customer_id=shadow.website_customer_id,
        email=shadow.email,
        first_name=shadow.first_name,
        last_name=shadow.last_name,
        phone_number=shadow.phone_number,
        customer_type=shadow.customer_type,
        description=shadow.description,
        company_name=shadow.company_name,
        tax_id=shadow.tax_id,
        address_street=shadow.address_street,
        address_ext_number=shadow.address_ext_number,
        address_int_number=shadow.address_int_number,
        address_neighborhood=shadow.address_neighborhood,
        address_city=shadow.address_city,
        address_state=shadow.address_state,
        address_postal_code=shadow.address_postal_code,
        address_country=shadow.address_country,
        is_active=shadow.is_active,
        source=shadow.source,
        created_at=shadow.created_at,
        updated_at=shadow.updated_at,
        current_seller_id=current_seller_id,
        current_seller_code=current_seller_code,
        current_seller_name=current_seller_name,
    )


def _log_domain_event(
    db: Session,
    *,
    event_type: str,
    entity_type: str,
    entity_id: str,
    payload: dict,
) -> None:
    event = DomainEvent(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        payload_json=payload,
    )
    db.add(event)


@router.post(
    "/sync",
    response_model=CustomerShadowOut,
    status_code=status.HTTP_200_OK,
)
def sync_customer_from_website(
    payload: CustomerSyncPayload,
    request: Request,
    db: Session = Depends(get_session),
) -> CustomerShadowOut:
    """Sync-endpoint aangeroepen vanuit de Website-module.

    - Upsert CustomerShadow op basis van website_customer_id.
    - Optioneel: (her)koppelen aan een Seller via seller_code.
    - Logt een DomainEvent voor auditeerbaarheid.
    """
    # Scope-check – placeholder; nu altijd OK.
    require_scope(request, "verkoop:admin")

    shadow = (
        db.query(CustomerShadow)
        .filter(CustomerShadow.website_customer_id == payload.website_customer_id)
        .first()
    )

    created = False
    if shadow is None:
        shadow = CustomerShadow(
            website_customer_id=payload.website_customer_id,
            email=str(payload.email),
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone_number=payload.phone_number,
            customer_type=payload.customer_type,
            description=payload.description,
            company_name=payload.company_name,
            tax_id=payload.tax_id,
            address_street=payload.address_street,
            address_ext_number=payload.address_ext_number,
            address_int_number=payload.address_int_number,
            address_neighborhood=payload.address_neighborhood,
            address_city=payload.address_city,
            address_state=payload.address_state,
            address_postal_code=payload.address_postal_code,
            address_country=payload.address_country,
            is_active=payload.is_active if payload.is_active is not None else True,
            source=payload.source,
        )
        db.add(shadow)
        created = True
    else:
        # Update bestaande shadow
        shadow.email = str(payload.email)
        shadow.first_name = payload.first_name
        shadow.last_name = payload.last_name
        shadow.phone_number = payload.phone_number
        shadow.customer_type = payload.customer_type
        shadow.description = payload.description
        shadow.company_name = payload.company_name
        shadow.tax_id = payload.tax_id
        shadow.address_street = payload.address_street
        shadow.address_ext_number = payload.address_ext_number
        shadow.address_int_number = payload.address_int_number
        shadow.address_neighborhood = payload.address_neighborhood
        shadow.address_city = payload.address_city
        shadow.address_state = payload.address_state
        shadow.address_postal_code = payload.address_postal_code
        shadow.address_country = payload.address_country
        if payload.is_active is not None:
            shadow.is_active = payload.is_active
        if payload.source is not None:
            shadow.source = payload.source

    # Event loggen
    _log_domain_event(
        db,
        event_type="CustomerSynced",
        entity_type="customer",
        entity_id=payload.website_customer_id,
        payload={
            "created": created,
            "website_customer_id": payload.website_customer_id,
            "seller_code": payload.seller_code,
        },
    )

    # Optionele verkoper-koppeling
    if payload.seller_code:
        _assign_customer_to_seller_internal(
            db=db,
            shadow=shadow,
            seller_code=payload.seller_code,
            assigned_by="sync",
            log_event=True,
            seller_id=None,
        )

    db.commit()
    db.refresh(shadow)
    return _build_customer_shadow_out(db, shadow)


def _assign_customer_to_seller_internal(
    *,
    db: Session,
    shadow: CustomerShadow,
    seller_code: Optional[str],
    seller_id: Optional[int] = None,
    assigned_by: Optional[str],
    log_event: bool,
) -> Optional[CustomerSellerAssignment]:
    if not seller_code and not seller_id:
        return None

    seller: Optional[Seller]
    if seller_id is not None:
        seller = db.query(Seller).get(seller_id)
    else:
        seller = (
            db.query(Seller)
            .filter(Seller.seller_code == seller_code)
            .first()
        )

    if seller is None:
        logger.warning(
            "Customer %s kon niet gekoppeld worden: seller niet gevonden (id=%s, code=%s)",
            shadow.website_customer_id,
            seller_id,
            seller_code,
        )
        return None

    now = datetime.utcnow()

    # Bestaande actieve assignment afsluiten
    existing = _get_active_assignment(db, shadow.id)
    if existing is not None:
        existing.unassigned_at = now
        db.add(existing)

    assignment = CustomerSellerAssignment(
        customer_id=shadow.id,
        seller_id=seller.id,
        assigned_at=now,
        assigned_by=assigned_by,
    )
    db.add(assignment)

    if log_event:
        _log_domain_event(
            db,
            event_type="CustomerAssignedToSeller",
            entity_type="customer",
            entity_id=shadow.website_customer_id,
            payload={
                "customer_id": shadow.id,
                "seller_id": seller.id,
                "seller_code": seller.seller_code,
                "assigned_by": assigned_by,
            },
        )

    return assignment


@router.get(
    "",
    response_model=CustomerListResponse,
)
def list_customers(
    request: Request,
    db: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Zoek op naam of e-mail"),
    seller_id: Optional[int] = Query(None, description="Filter op actieve seller-id"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> CustomerListResponse:
    """Admin-lijst van klanten in de verkoopmodule."""
    require_scope(request, "verkoop:admin")

    query = db.query(CustomerShadow)

    if search:
        like = f"%{search.lower()}%"
        from sqlalchemy import func, or_

        query = query.filter(
            or_(
                func.lower(CustomerShadow.email).like(like),
                func.lower(CustomerShadow.first_name).like(like),
                func.lower(CustomerShadow.last_name).like(like),
            )
        )

    if seller_id is not None:
        # Join op actieve assignment
        query = query.join(
            CustomerSellerAssignment,
            (CustomerSellerAssignment.customer_id == CustomerShadow.id)
            & (CustomerSellerAssignment.unassigned_at.is_(None)),
        ).filter(CustomerSellerAssignment.seller_id == seller_id)

    total = query.count()

    shadows: List[CustomerShadow] = (
        query.order_by(CustomerShadow.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items: List[CustomerListItem] = []
    for shadow in shadows:
        assignment = _get_active_assignment(db, shadow.id)
        current_seller_id = None
        current_seller_code = None
        current_seller_name = None
        if assignment is not None:
            seller = db.query(Seller).get(assignment.seller_id)
            if seller is not None:
                current_seller_id = seller.id
                current_seller_code = seller.seller_code
                full_name_parts = [seller.first_name, seller.last_name]
                current_seller_name = " ".join(p for p in full_name_parts if p)

        items.append(
            CustomerListItem(
                id=shadow.id,
                website_customer_id=shadow.website_customer_id,
                email=shadow.email,
                first_name=shadow.first_name,
                last_name=shadow.last_name,
                customer_type=shadow.customer_type,
                company_name=shadow.company_name,
                is_active=shadow.is_active,
                source=shadow.source,
                current_seller_id=current_seller_id,
                current_seller_code=current_seller_code,
                current_seller_name=current_seller_name,
                created_at=shadow.created_at,
            )
        )

    return CustomerListResponse(items=items, total=total)


@router.get(
    "/{customer_id}",
    response_model=CustomerShadowOut,
)
def get_customer(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_session),
) -> CustomerShadowOut:
    """Detail van één klant."""
    require_scope(request, "verkoop:admin")

    shadow = db.query(CustomerShadow).get(customer_id)
    if shadow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    return _build_customer_shadow_out(db, shadow)


@router.get(
    "/{customer_id}/assignments",
    response_model=list[CustomerAssignmentHistoryItem],
)
def get_customer_assignments(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_session),
) -> list[CustomerAssignmentHistoryItem]:
    """Historiek van seller-assignments voor een klant."""
    require_scope(request, "verkoop:admin")

    # Zorg dat klant bestaat
    shadow = db.query(CustomerShadow).get(customer_id)
    if shadow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    assignments: List[CustomerSellerAssignment] = (
        db.query(CustomerSellerAssignment)
        .filter(CustomerSellerAssignment.customer_id == customer_id)
        .order_by(CustomerSellerAssignment.assigned_at.asc())
        .all()
    )

    history: List[CustomerAssignmentHistoryItem] = []
    for a in assignments:
        seller = db.query(Seller).get(a.seller_id)
        seller_code = seller.seller_code if seller else ""
        full_name_parts = (
            [getattr(seller, "first_name", None), getattr(seller, "last_name", None)]
            if seller
            else []
        )
        seller_name = " ".join(p for p in full_name_parts if p)

        history.append(
            CustomerAssignmentHistoryItem(
                id=a.id,
                seller_id=a.seller_id,
                seller_code=seller_code,
                seller_name=seller_name,
                assigned_at=a.assigned_at,
                unassigned_at=a.unassigned_at,
                assigned_by=a.assigned_by,
            )
        )

    return history


@router.post(
    "/{customer_id}/assign",
    response_model=CustomerShadowOut,
    status_code=status.HTTP_200_OK,
)
def assign_customer_to_seller(
    customer_id: int,
    payload: CustomerAssignmentRequest,
    request: Request,
    db: Session = Depends(get_session),
) -> CustomerShadowOut:
    """Koppel (of her-koppel) een klant aan een verkoper."""
    ctx = require_scope(request, "verkoop:admin")

    shadow = db.query(CustomerShadow).get(customer_id)
    if shadow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    seller_id, seller_code = payload.resolve_target()
    if not seller_id and not seller_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="seller_id of seller_code is verplicht",
        )

    assigned_by = payload.assigned_by or ctx.sub

    _assign_customer_to_seller_internal(
        db=db,
        shadow=shadow,
        seller_code=seller_code,
        seller_id=seller_id,
        assigned_by=assigned_by,
        log_event=True,
    )

    db.commit()
    db.refresh(shadow)
    return _build_customer_shadow_out(db, shadow)
