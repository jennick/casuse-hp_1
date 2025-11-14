
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.payment import PaymentIntent
from app.services.payments.providers import ProviderFactory
from app.core.config import settings
from app.core.security import require_scope

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/intent/{order_id}")
def create_intent(order_id: int, request: Request, db: Session = Depends(get_session)):
    _ = require_scope(request, "verkoop:write")
    provider = ProviderFactory.get(settings.PAYMENTS_PROVIDER)
    res = provider.create_intent(amount=100.00)
    pi = PaymentIntent(order_id=order_id, provider=settings.PAYMENTS_PROVIDER, intent_id=res.intent_id, amount=100.00, currency="MXN", status=res.status, metadata={})
    db.add(pi); db.commit(); db.refresh(pi)
    return {"intent_id": pi.intent_id, "status": pi.status, "payment_url": res.payment_url}

@router.post("/webhook")
def webhook(payload: dict):
    return {"ok": True}
