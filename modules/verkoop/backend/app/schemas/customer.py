# verkoop/backend/app/schemas/customer.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerShadowBase(BaseModel):
    website_customer_id: str = Field(..., min_length=1)
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

    customer_type: str
    description: Optional[str] = None
    company_name: Optional[str] = None
    tax_id: Optional[str] = None

    address_street: Optional[str] = None
    address_ext_number: Optional[str] = None
    address_int_number: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_postal_code: Optional[str] = None
    address_country: Optional[str] = None

    is_active: bool = True
    source: Optional[str] = None


class CustomerShadowOut(CustomerShadowBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Huidige verkoper (indien toegewezen)
    current_seller_id: Optional[int] = None
    current_seller_code: Optional[str] = None
    current_seller_name: Optional[str] = None

    class Config:
        orm_mode = True


class CustomerListItem(BaseModel):
    id: int
    website_customer_id: str
    email: EmailStr
    first_name: str
    last_name: str
    customer_type: str
    company_name: Optional[str] = None
    is_active: bool
    source: Optional[str] = None

    current_seller_id: Optional[int] = None
    current_seller_code: Optional[str] = None
    current_seller_name: Optional[str] = None

    created_at: datetime

    class Config:
        orm_mode = True


class CustomerListResponse(BaseModel):
    items: List[CustomerListItem]
    total: int


class CustomerAssignmentHistoryItem(BaseModel):
    id: int
    seller_id: int
    seller_code: str
    seller_name: str
    assigned_at: datetime
    unassigned_at: Optional[datetime] = None
    assigned_by: Optional[str] = None

    class Config:
        orm_mode = True


class CustomerAssignmentRequest(BaseModel):
    seller_id: Optional[int] = None
    seller_code: Optional[str] = None
    assigned_by: Optional[str] = None

    def resolve_target(self) -> tuple[Optional[int], Optional[str]]:
        return self.seller_id, self.seller_code


class CustomerSyncPayload(BaseModel):
    website_customer_id: str = Field(..., min_length=1)

    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

    customer_type: str
    description: Optional[str] = None
    company_name: Optional[str] = None
    tax_id: Optional[str] = None

    address_street: Optional[str] = None
    address_ext_number: Optional[str] = None
    address_int_number: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_postal_code: Optional[str] = None
    address_country: Optional[str] = None

    is_active: Optional[bool] = True
    source: Optional[str] = "website_form"

    # Optioneel: koppeling naar verkoper
    seller_code: Optional[str] = None
