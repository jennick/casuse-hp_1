from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator
from models import CustomerType


# =====================================================
# Auth / Token
# =====================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[EmailStr] = None

    # ⚠️ intern technisch ID (wordt later uitgefaseerd)
    customer_id: Optional[str] = None

    # 🔐 extern, stabiel klant-ID (COMMIT 2)
    customer_uuid: Optional[UUID] = None

    is_admin: Optional[bool] = None


# =====================================================
# Public registration
# =====================================================

class RegistrationRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    customer_type: CustomerType
    description: str

    company_name: Optional[str] = None
    tax_id: Optional[str] = None

    address_street: str
    address_ext_number: str
    address_int_number: Optional[str] = None
    address_neighborhood: str
    address_city: str
    address_state: str
    address_postal_code: str
    address_country: str

    @validator("company_name", "tax_id", always=True)
    def validate_company_fields(cls, v, values, field):
        """
        Voor customer_type=bedrijf zijn company_name en tax_id verplicht.
        Voor particulier mogen ze leeg zijn.
        """
        customer_type = values.get("customer_type")
        if customer_type == CustomerType.bedrijf:
            if not v or not str(v).strip():
                raise ValueError(
                    "Bedrijfsnaam en BTW / RFC zijn verplicht voor zakelijke klanten."
                )
        return v


class RegistrationResponse(BaseModel):
    status: str
    message: str
    registration_id: str


# =====================================================
# Password setup
# =====================================================

class PasswordSetupTokenInfo(BaseModel):
    status: str
    email: EmailStr


class PasswordSetupRequest(BaseModel):
    password: str
    password_confirm: str


class PasswordSetupResponse(BaseModel):
    status: str
    message: str


# =====================================================
# Public login
# =====================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =====================================================
# Admin / customers – base
# =====================================================

class CustomerBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    customer_type: CustomerType
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


class CustomerCreate(CustomerBase):
    # eventueel direct wachtwoord zetten via admin (nu nog niet gebruikt)
    password: Optional[str] = None


class CustomerUpdate(BaseModel):
    # partial update
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    customer_type: Optional[CustomerType] = None
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

    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


# =====================================================
# Admin / customers – list
# =====================================================

class CustomerListItem(BaseModel):
    id: UUID                          # intern
    customer_uuid: UUID               # 🔐 extern (COMMIT 2)

    email: EmailStr
    first_name: str
    last_name: str
    customer_type: CustomerType
    is_active: bool
    created_at: datetime

    company_name: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None

    # login / portal status
    has_login: bool
    portal_status: Optional[str] = None
    deactivated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CustomersListResponse(BaseModel):
    items: List[CustomerListItem]
    total: int


# =====================================================
# Admin / customers – detail
# =====================================================

class CustomerResponse(CustomerBase):
    id: UUID                          # intern
    customer_uuid: UUID               # 🔐 extern (COMMIT 2)

    is_active: bool
    is_admin: bool

    created_at: datetime
    updated_at: datetime

    # extra metadata
    deactivated_at: Optional[datetime] = None
    hashed_password: Optional[str] = None

    # login / portal status
    has_login: bool
    portal_status: Optional[str] = None

    class Config:
        orm_mode = True


# =====================================================
# Generic responses
# =====================================================

class SimpleSuccessResponse(BaseModel):
    success: bool


class PasswordResetResponse(BaseModel):
    success: bool
    # In local/dev mag de backend de token meesturen (debugging in UI)
    token: Optional[str] = None
