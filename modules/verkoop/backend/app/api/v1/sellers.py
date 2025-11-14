
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerUpdate, SellerOut
from app.core.security import require_scope

router = APIRouter(prefix="/sellers", tags=["sellers"])

@router.get("", response_model=list[SellerOut])
def list_sellers(request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:read")
    return db.query(Seller).all()

@router.post("", response_model=SellerOut, status_code=201)
def create_seller(payload: SellerCreate, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:admin")
    s = Seller(**payload.model_dump())
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.patch("/{seller_id}", response_model=SellerOut)
def update_seller(seller_id: int, payload: SellerUpdate, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:admin")
    s = db.query(Seller).get(seller_id)
    if not s: raise HTTPException(404, "Not found")
    for k,v in payload.model_dump(exclude_none=True).items():
        setattr(s,k,v)
    db.add(s); db.commit(); db.refresh(s)
    return s
