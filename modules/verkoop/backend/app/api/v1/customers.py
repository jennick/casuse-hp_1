from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models.customer import CustomerShadow

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("")
def list_customers(db: Session = Depends(get_session)):
    items = (
        db.query(CustomerShadow)
        .order_by(CustomerShadow.created_at.desc())
        .all()
    )

    return {
        "items": items,
        "total": len(items),
    }


@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_session)):
    customer = (
        db.query(CustomerShadow)
        .filter(CustomerShadow.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer
