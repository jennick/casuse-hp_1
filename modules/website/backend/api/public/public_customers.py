from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from deps import get_db
import crud
from schemas import CustomersListResponse, CustomerListItem

router = APIRouter(
    prefix="/api/public/customers",
    tags=["Public Customers"],
)


@router.get("/", response_model=CustomersListResponse)
def public_list_customers(
    db: Session = Depends(get_db),
    search: str | None = Query(None),
    customer_type: str | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    """
    Publieke read-only API voor andere modules (bv. verkoop).

    BELANGRIJK:
    - Enkel klanten met een afgeronde registratie
    - = actief + wachtwoord ingesteld
    """

    items, _ = crud.list_customers(
        db=db,
        search=search,
        customer_type=customer_type,
        skip=skip,
        limit=limit,
        status="active",
        sort_by="created_at",
        sort_dir="desc",
    )

    # 🔒 KRITIEKE FILTER:
    # enkel klanten die effectief kunnen inloggen
    completed_customers = [
        customer for customer in items if customer.has_login
    ]

    return CustomersListResponse(
        items=[
            CustomerListItem.from_orm(customer)
            for customer in completed_customers
        ],
        total=len(completed_customers),
    )
