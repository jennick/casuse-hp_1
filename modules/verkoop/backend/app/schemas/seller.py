from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SellerBase(BaseModel):
    seller_code: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email_work: EmailStr
    phone_mobile: str = Field(..., max_length=50)
    phone_internal: Optional[str] = Field(None, max_length=50)

    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    postal_code: str = Field(..., max_length=20)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=2, description="ISO-landcode, bv. 'BE'")

    region_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Interne regiocode, bv. BE-VOV of MX-CMX",
    )
    employment_type: Optional[str] = Field(
        None,
        max_length=50,
        description="Type tewerkstelling: intern, extern, agent, ...",
    )

    max_discount_percent: float = Field(
        0,
        ge=0,
        le=100,
        description="Maximale commercieel toegelaten korting in %",
    )
    default_margin_target_percent: float = Field(
        0,
        ge=0,
        le=100,
        description="Streefdoel marge in %",
    )


class SellerCreate(SellerBase):
    """Payload voor het aanmaken van een nieuwe verkoper vanuit de admin-module."""

    # bij create is een code verplicht
    seller_code: str = Field(..., max_length=50)

    # intern nummer wordt in het model zelf gegenereerd, niet via de API
    # daarom staat het niet in dit schema


class SellerUpdate(SellerBase):
    """Payload voor het bijwerken van een bestaande verkoper.

    Alle velden zijn optioneel zodat we partial updates kunnen doen.
    """

    seller_code: Optional[str] = Field(None, max_length=50)
    email_work: Optional[EmailStr] = None
    phone_mobile: Optional[str] = Field(None, max_length=50)
    phone_internal: Optional[str] = Field(None, max_length=50)

    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    postal_code: Optional[str] = Field(None, max_length=20)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=2)

    region_code: Optional[str] = Field(None, max_length=50)
    employment_type: Optional[str] = Field(None, max_length=50)

    max_discount_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
    )
    default_margin_target_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
    )

    # status & rol worden in de API vaak apart beheerd,
    # maar we laten ze hier optioneel toe zodat je ze vanuit de UI kunt wijzigen
    is_active: Optional[bool] = None
    role: Optional[str] = Field(
        None,
        max_length=20,
        description="seller / manager / admin ...",
    )


class SellerOut(SellerBase):
    """Representatie van een verkoper naar de frontend."""

    id: int
    internal_number: Optional[int] = Field(
        None,
        description="Intern uniek nummer dat automatisch wordt toegekend.",
    )
    is_active: bool
    role: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SellerPasswordResetRequest(BaseModel):
    """Payload voor het instellen van een nieuw wachtwoord op basis van een reset-token.

    Wordt gebruikt door de endpoint `POST /api/v1/sellers/reset-password`.
    De frontend stuurt in ieder geval `token` en `new_password`.
    Als er extra velden meegestuurd worden (bv. confirm-veld),
    worden die door Pydantic genegeerd.
    """

    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)
