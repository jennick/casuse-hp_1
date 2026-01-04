import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    Enum,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# =====================================================
# Helpers
# =====================================================

def utcnow():
    return datetime.now(timezone.utc)


# =====================================================
# Enums
# =====================================================

class CustomerType(str, enum.Enum):
    particulier = "particulier"
    bedrijf = "bedrijf"


# =====================================================
# Customer
# =====================================================

class Customer(Base):
    __tablename__ = "customers"

    # -------------------------------------------------
    # Interne technische primary key
    # -------------------------------------------------
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------
    # 🔐 Extern, stabiel klant-ID (COMMIT 1)
    # -------------------------------------------------
    customer_uuid = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        index=True,
        server_default=func.gen_random_uuid(),
    )

    # -------------------------------------------------
    # Identiteit & login
    # -------------------------------------------------
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)

    # -------------------------------------------------
    # Basisgegevens
    # -------------------------------------------------
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=True)

    customer_type = Column(Enum(CustomerType), nullable=False)
    description = Column(Text, nullable=True)

    # -------------------------------------------------
    # Status / rechten
    # -------------------------------------------------
    is_active = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    # -------------------------------------------------
    # Bedrijfsgegevens
    # -------------------------------------------------
    company_name = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)

    # -------------------------------------------------
    # Adres
    # -------------------------------------------------
    address_street = Column(String(255), nullable=True)
    address_ext_number = Column(String(50), nullable=True)
    address_int_number = Column(String(50), nullable=True)
    address_neighborhood = Column(String(255), nullable=True)
    address_city = Column(String(255), nullable=True)
    address_state = Column(String(255), nullable=True)
    address_postal_code = Column(String(20), nullable=True)
    address_country = Column(String(100), nullable=False, default="Mexico")

    # -------------------------------------------------
    # Timestamps
    # -------------------------------------------------
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )

    # -------------------------------------------------
    # Relaties
    # -------------------------------------------------
    registration_tokens = relationship(
        "RegistrationToken",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "CustomerDocument",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    # -------------------------------------------------
    # Helpers voor admin / portal (GEEN DB-kolommen)
    # -------------------------------------------------

    @property
    def has_portal_password(self) -> bool:
        """
        Geeft aan of deze klant al een wachtwoord heeft ingesteld
        (dus effectief kan inloggen in het portaal).
        """
        return self.hashed_password is not None

    @property
    def has_login(self) -> bool:
        """
        Alias voor has_portal_password, zodat Pydantic-schemas
        het veld 'has_login' via from_orm kunnen gebruiken.
        """
        return self.has_portal_password

    @property
    def latest_registration_token(self):
        """
        Geeft het meest recente registratietoken terug (of None).
        """
        if not self.registration_tokens:
            return None
        return max(self.registration_tokens, key=lambda t: t.created_at)

    @property
    def portal_status(self) -> str:
        """
        Afgeleide status voor admin-weergave.

        Mogelijke waarden:
        - active
        - invited
        - invitation_expired
        - no_invitation
        """
        if self.has_portal_password and self.is_active:
            return "active"

        token = self.latest_registration_token
        if token is None:
            return "no_invitation"

        if token.used:
            return "no_invitation"

        if token.expires_at < utcnow():
            return "invitation_expired"

        return "invited"


# =====================================================
# RegistrationToken
# =====================================================

class RegistrationToken(Base):
    __tablename__ = "registration_tokens"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )

    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

    customer = relationship(
        "Customer",
        back_populates="registration_tokens",
    )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < utcnow()


# =====================================================
# CustomerDocument
# =====================================================

class CustomerDocument(Base):
    __tablename__ = "customer_documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    customer = relationship(
        "Customer",
        back_populates="documents",
    )
