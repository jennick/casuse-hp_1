
from pydantic import BaseModel

class OrderCreate(BaseModel):
    quote_id: int
    seller_book_no: str | None = None

class OrderOut(BaseModel):
    id: int
    order_no: str | None = None
    total: float
    status: str
    class Config:
        from_attributes = True
