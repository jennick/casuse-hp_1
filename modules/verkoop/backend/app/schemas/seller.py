
from pydantic import BaseModel, Field, EmailStr

class SellerBase(BaseModel):
    code: str = Field(..., max_length=32)
    name: str
    email: EmailStr
    avatar_url: str | None = None
    max_discount_percent: float = 10.0
    active: bool = True

class SellerCreate(SellerBase):
    pass

class SellerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    avatar_url: str | None = None
    max_discount_percent: float | None = None
    active: bool | None = None

class SellerOut(SellerBase):
    id: int
    class Config:
        from_attributes = True
