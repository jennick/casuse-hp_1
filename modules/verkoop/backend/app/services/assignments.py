
from sqlalchemy.orm import Session
from app.models.customer import CustomerAssignment
from sqlalchemy import select

def list_assignments(db: Session, seller_id: int | None = None, status: str | None = None):
    q = select(CustomerAssignment)
    if seller_id: q = q.where(CustomerAssignment.seller_id == seller_id)
    if status: q = q.where(CustomerAssignment.status == status)
    return db.execute(q).scalars().all()
