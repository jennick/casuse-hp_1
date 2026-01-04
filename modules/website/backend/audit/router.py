
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from deps import get_db
from security import decode_access_token
from .models import AuditEvent

router = APIRouter(
    prefix="/api/admin/customers",
    tags=["Audit"]
)

def require_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

@router.get("/{customer_id}/events")
def get_events(customer_id: str, db: Session = Depends(get_db), admin=Depends(require_admin)):
    events = (
        db.query(AuditEvent)
        .filter(AuditEvent.customer_id == customer_id)
        .order_by(AuditEvent.created_at.desc())
        .all()
    )
    return [
        {
            "id": e.id,
            "actor": e.actor,
            "action": e.action,
            "description": e.description,
            "created_at": e.created_at,
        }
        for e in events
    ]
