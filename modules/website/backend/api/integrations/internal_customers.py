from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from deps import get_db
from models import Customer
from schemas import CustomersListResponse, CustomerListItem
from config import settings
import crud

router = APIRouter(
    prefix="/api/internal/customers",
    tags=["Internal Customers"],
)


def verify_internal_key(internal_key: Optional[str]):
    """Beveiliging: verplicht 'X-Internal-Key' header."""
    if internal_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid internal key")


@router.get("/", response_model=CustomersListResponse)
def internal_list_customers(
    db: Session = Depends(get_db),
    internal_key: str = Header(None, alias="X-Internal-Key"),
):
    verify_internal_key(internal_key)

    items, total = crud.list_customers(
        db=db,
        search=None,
        customer_type=None,
        skip=0,
        limit=5000,
        status="active",
        sort_by="created_at",
        sort_dir="desc",
    )

    return CustomersListResponse(
        items=[CustomerListItem.from_orm(c) for c in items],
        total=total,
    )


@router.get("/{customer_id}", response_model=CustomerListItem)
def internal_get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    internal_key: str = Header(None, alias="X-Internal-Key"),
):
    verify_internal_key(internal_key)

    customer: Customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Not found")

    return CustomerListItem.from_orm(customer)
