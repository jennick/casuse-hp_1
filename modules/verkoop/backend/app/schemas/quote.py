
from pydantic import BaseModel
from typing import List

class QuoteLineIn(BaseModel):
    product_id: int
    qty: int
    discount_percent: float = 0.0

class QuoteCreate(BaseModel):
    customer_id: int | None = None
    seller_id: int | None = None
    currency: str = "MXN"
    lines: List[QuoteLineIn] = []

class QuoteOut(BaseModel):
    id: int
    quote_no: str | None = None
    subtotal: float
    vat: float
    total: float
    status: str
    class Config:
        from_attributes = True
