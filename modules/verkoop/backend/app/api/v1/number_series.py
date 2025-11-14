
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.services.number_series import reserve_number
from app.schemas.number_series import ReserveNumberRequest, ReservedNumber
from app.core.security import require_scope

router = APIRouter(prefix="/number_series", tags=["number_series"])

@router.post("/reserve", response_model=ReservedNumber)
def reserve(req: ReserveNumberRequest, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:write")
    n = reserve_number(db, req.series_name.upper())
    db.commit()
    return {"number": n}
