
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.assignments import list_assignments
from app.core.security import require_scope

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.get("")
def list_all(seller_id: int | None = None, status: str | None = None, request: Request = None, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:read")
    data = list_assignments(db, seller_id=seller_id, status=status)
    return [{"id": a.id, "customer_id": a.customer_id, "seller_id": a.seller_id, "status": a.status, "auto_assigned": a.auto_assigned} for a in data]
