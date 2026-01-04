
from fastapi import APIRouter, Depends, HTTPException, Header
from security import decode_access_token
from .service import get_customer_documents

router = APIRouter(
    prefix="/api/admin/customers",
    tags=["Documents"]
)

def require_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

@router.get("/{customer_id}/documents")
def list_documents(customer_id: str, admin=Depends(require_admin)):
    return get_customer_documents(customer_id)
