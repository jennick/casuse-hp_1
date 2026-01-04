from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid

from deps import get_db, get_current_admin_user
from models import Customer, CustomerDocument
from schemas import CustomerResponse, CustomerUpdate
import crud

router = APIRouter(
    prefix="/api/admin/customers",
    tags=["Admin Customers"],
)

# =====================================================
# CUSTOMER DETAIL
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


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Admin – update klant",
)
def admin_update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdate,
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

# =====================================================
# CUSTOMER DOCUMENTS
# =====================================================

@router.get(
    "/{customer_id}/documents",
    summary="Admin – lijst documenten van klant",
)
def admin_list_customer_documents(
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

    documents = (
        db.query(CustomerDocument)
        .filter(
            CustomerDocument.customer_id == customer_id,
            CustomerDocument.deleted_at.is_(None),
        )
        .order_by(CustomerDocument.created_at.desc())
        .all()
    )

    return documents


@router.delete(
    "/{customer_id}/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Admin – verwijder document (soft delete)",
)
def admin_delete_customer_document(
    customer_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: Customer = Depends(get_current_admin_user),
):
    document = (
        db.query(CustomerDocument)
        .filter(
            CustomerDocument.id == document_id,
            CustomerDocument.customer_id == customer_id,
            CustomerDocument.deleted_at.is_(None),
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    document.deleted_at = datetime.now(timezone.utc)
    db.add(document)
    db.commit()

    return None
