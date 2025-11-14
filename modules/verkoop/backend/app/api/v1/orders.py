
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.order import OrderCreate, OrderOut
from app.models.order import SalesOrder, SalesOrderLine
from app.models.quote import Quote, QuoteLine
from app.services.number_series import reserve_number
from app.core.security import require_scope

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:write")
    q = db.query(Quote).get(payload.quote_id)
    if not q: raise HTTPException(400, "Quote missing")
    o = SalesOrder(customer_id=q.customer_id, seller_id=q.seller_id,
                   subtotal=q.subtotal, vat=q.vat, total=q.total, status="created",
                   seller_book_no=payload.seller_book_no)
    db.add(o); db.flush()
    for l in db.query(QuoteLine).filter(QuoteLine.quote_id==q.id).all():
        db.add(SalesOrderLine(order_id=o.id, product_id=l.product_id, qty=l.qty,
                              unit_price=l.unit_price, discount_percent=l.discount_percent, line_total=l.line_total))
    o.order_no = reserve_number(db, "ORDER")
    db.commit(); db.refresh(o)
    return o
