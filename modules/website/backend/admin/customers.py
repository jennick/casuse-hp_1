from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
    Body,
)
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from deps import get_db, get_current_admin_user
from models import Customer, CustomerType
import crud
from schemas import (
    CustomersListResponse,
    CustomerResponse,
    CustomerUpdate,
)

router = APIRouter(
    prefix="/api/admin/customers",
    tags=["Admin Customers"],
)

# =====================================================
# LIST
# =====================================================

@router.get(
    "/",
    response_model=CustomersListResponse,
    summary="Admin – lijst alle klanten",
)
def admin_list_customers(
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_current_admin_user),

    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),

    search: Optional[str] = Query(None),
    customer_type: Optional[CustomerType] = Query(None),
    status: str = Query("all", pattern="^(active|inactive|all)$"),

    sort_by: str = Query("created_at", pattern="^(created_at|name)$"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"),
):
    items, total = crud.list_customers(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        customer_type=customer_type,
        status=status,
        sort_by=sort_by,
        sort_dir=sort_dir,
        visibility="admin",
    )

    return CustomersListResponse(
        items=items,
        total=total,
    )

# =====================================================
# DETAIL
# =====================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Admin – klant detail",
)
def admin_get_customer(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_current_admin_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer

# =====================================================
# UPDATE
# =====================================================

@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Admin – update klant",
)
def admin_update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdate = Body(...),  # ✅ CRUCIAAL
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_current_admin_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return crud.update_customer(db, customer, payload)
