# verkoop/backend/app/services/assignments.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import CustomerSellerAssignment


def list_assignments(
    db: Session,
    seller_id: Optional[int] = None,
    status: Optional[str] = None,
) -> List[CustomerSellerAssignment]:
    """Listeer klant-verkoper-assignments.

    status:
        - None / "all"  : alle assignments
        - "active"      : alleen huidige actieve (unassigned_at IS NULL)
        - "inactive"    : alleen historisch (unassigned_at IS NOT NULL)
    """
    stmt = select(CustomerSellerAssignment)

    if seller_id is not None:
        stmt = stmt.where(CustomerSellerAssignment.seller_id == seller_id)

    if status == "active":
        stmt = stmt.where(CustomerSellerAssignment.unassigned_at.is_(None))
    elif status == "inactive":
        stmt = stmt.where(CustomerSellerAssignment.unassigned_at.is_not(None))

    return db.execute(stmt).scalars().all()
