
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import uuid
from deps import get_db
from security import decode_access_token
from .models import CustomerModuleRelation

router = APIRouter(
    prefix="/api/admin/customers",
    tags=["Relations"]
)

def require_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

@router.get("/{customer_id}/relations")
def list_relations(customer_id: str, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(CustomerModuleRelation).filter_by(customer_id=customer_id).all()
