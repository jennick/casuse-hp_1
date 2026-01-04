import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.customer_sync import (
    fetch_customers_from_website,
    sync_customers_into_verkoop,
)

router = APIRouter(
    prefix="/customers-sync",
    tags=["Customer Sync"],
)

logger = logging.getLogger(__name__)


@router.get("/preview")
async def preview_customers():
    customers = await fetch_customers_from_website()
    return {
        "count": len(customers),
        "items": customers,
    }


@router.post("/run")
async def run_sync(db: Session = Depends(get_session)):
    customers = await fetch_customers_from_website()
    result = sync_customers_into_verkoop(db, customers)
    return result
