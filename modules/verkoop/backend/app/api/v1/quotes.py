
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.quote import QuoteCreate, QuoteOut
from app.models.quote import Quote, QuoteLine
from app.services.pricing import price_quote
from app.services.number_series import reserve_number
from app.core.security import require_scope

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.post("", response_model=QuoteOut, status_code=201)
def create_quote(payload: QuoteCreate, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:write")
    calc = price_quote(db, [l.dict() for l in payload.lines])
    q = Quote(customer_id=payload.customer_id, seller_id=payload.seller_id,
              subtotal=calc['subtotal'], vat=calc['vat'], total=calc['total'], status="draft")
    db.add(q); db.flush()
    # create lines
    for l in payload.lines:
        # minimal unit price fetch again
        from app.models.catalog import ProductCatalog
        p = db.query(ProductCatalog).get(l.product_id)
        unit = float(p.base_price) if p else 0.0
        line_total = next((x['line_total'] for x in calc['lines'] if x['sku']==p.sku), 0.0) if p else 0.0
        db.add(QuoteLine(quote_id=q.id, product_id=l.product_id, qty=l.qty, unit_price=unit, discount_percent=l.discount_percent, line_total=line_total))
    db.commit(); db.refresh(q)
    return q

@router.post("/{quote_id}/reserve_number", response_model=QuoteOut)
def finalize_quote(quote_id: int, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:write")
    q = db.query(Quote).get(quote_id)
    if not q: raise HTTPException(404, "Not found")
    if not q.quote_no:
        q.quote_no = reserve_number(db, "QUOTE")
    q.status = "final"
    db.add(q); db.commit(); db.refresh(q)
    return q
