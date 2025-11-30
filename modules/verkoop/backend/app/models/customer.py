# verkoop/backend/app/models/customer.py

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class CustomerShadow(Base):
    """Lokale kopie van een Customer uit de Website-module.

    Deze tabel bevat zowel particuliere als bedrijfs-klanten, inclusief
    contact- en adresgegevens. De Website-module blijft de bron van waarheid;
    dit is enkel een shadow in de verkoop-module.
    """

    __tablename__ = "customer_shadows"

    id: int = Column(Integer, primary_key=True, index=True)

    website_customer_id: str = Column(
        String(36),
        nullable=False,
        unique=True,
        index=True,
        doc="UUID van de Website Customer als string",
    )

    # Basisidentiteit
    email: str = Column(String(255), nullable=False, index=True)
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    phone_number: Optional[str] = Column(String(50), nullable=True)

    # Klanttype & bedrijf
    customer_type: str = Column(
        String(50),
        nullable=False,
        doc="particulier / bedrijf – stringwaarde van Website.CustomerType",
    )
    description: Optional[str] = Column(Text, nullable=True)
    company_name: Optional[str] = Column(String(255), nullable=True)
    tax_id: Optional[str] = Column(String(50), nullable=True)

    # Adres
    address_street: Optional[str] = Column(String(255), nullable=True)
    address_ext_number: Optional[str] = Column(String(50), nullable=True)
    address_int_number: Optional[str] = Column(String(50), nullable=True)
    address_neighborhood: Optional[str] = Column(String(255), nullable=True)
    address_city: Optional[str] = Column(String(255), nullable=True)
    address_state: Optional[str] = Column(String(255), nullable=True)
    address_postal_code: Optional[str] = Column(String(20), nullable=True)
    address_country: Optional[str] = Column(String(100), nullable=True)

    # Status / meta
    is_active: bool = Column(Boolean, nullable=False, server_default="true")
    source: Optional[str] = Column(
        String(50),
        nullable=True,
        doc="website_form / sales_app / import / ...",
    )

    created_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relaties
    assignments = relationship(
        "CustomerSellerAssignment",
        back_populates="customer",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<CustomerShadow id={self.id} website_customer_id={self.website_customer_id} "
            f"email={self.email!r} type={self.customer_type!r}>"
        )


class CustomerSellerAssignment(Base):
    """Historische koppeling tussen een CustomerShadow en een Seller.

    Elke klant kan meerdere assignments hebben in de tijd.
    De 'actieve' koppeling is die waar unassigned_at NULL is.
    """

    __tablename__ = "customer_seller_assignments"

    id: int = Column(Integer, primary_key=True, index=True)
    customer_id: int = Column(
        Integer,
        ForeignKey("customer_shadows.id", ondelete="CASCADE"),
        nullable=False,
    )
    seller_id: int = Column(
        Integer,
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
    )

    assigned_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    assigned_by: Optional[str] = Column(
        String(255),
        nullable=True,
        doc="Wie heeft toegewezen (bv. 'sync', 'system' of user-id).",
    )
    unassigned_at: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="NULL = huidige actieve assignment.",
    )

    customer = relationship(
        "CustomerShadow",
        back_populates="assignments",
        lazy="joined",
    )
    seller = relationship(
        "Seller",
        back_populates="assignments",
        lazy="joined",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<CustomerSellerAssignment id={self.id} customer_id={self.customer_id} "
            f"seller_id={self.seller_id} assigned_at={self.assigned_at} "
            f"unassigned_at={self.unassigned_at}>"
        )
