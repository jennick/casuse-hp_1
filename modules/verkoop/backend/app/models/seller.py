from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Seller(Base):
    __tablename__ = "sellers"

    # --- primaire sleutel ---
    id: int = Column(Integer, primary_key=True, index=True)

    # --- business code & intern nummer ---
    # Externe code (zichtbaar in UI, bv. S-0003)
    seller_code: str = Column(String(50), nullable=False, unique=True, index=True)

    # Intern nummer (NULL toestaan omdat frontend dit niet invult)
    internal_number: Optional[str] = Column(
        String(50),
        nullable=True,
        unique=True,
        index=True,
    )

    # --- basisgegevens ---
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    email_work: str = Column(String(255), nullable=False, unique=True, index=True)

    phone_mobile: str = Column(String(50), nullable=False)
    phone_internal: Optional[str] = Column(String(50), nullable=True)

    # --- adres ---
    address_line1: str = Column(String(255), nullable=False)
    address_line2: Optional[str] = Column(String(255), nullable=True)
    postal_code: Optional[str] = Column(String(20), nullable=True)
    city: Optional[str] = Column(String(100), nullable=True)
    country: Optional[str] = Column(String(2), nullable=True)
    region_code: Optional[str] = Column(String(50), nullable=True)

    # --- tewerkstelling & commerciële parameters ---
    employment_type: Optional[str] = Column(String(20), nullable=True)
    max_discount_percent: Optional[int] = Column(Integer, nullable=True)
    default_margin_target_percent: Optional[int] = Column(Integer, nullable=True)

    # --- status & rol ---
    is_active: bool = Column(Boolean, nullable=False, server_default="true")
    role: str = Column(String(20), nullable=False, server_default="seller")

    # --- AUTH: wachtwoord & reset-token ---
    password_hash: Optional[str] = Column(String(255), nullable=True)
    reset_token: Optional[str] = Column(String(255), nullable=True, index=True)
    reset_token_expires_at: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # --- Relatie naar klant-assignments ---
    assignments = relationship(
        "CustomerSellerAssignment",
        back_populates="seller",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # --- timestamps ---
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

    def __repr__(self) -> str:
        return (
            f"<Seller id={self.id} code={self.seller_code!r} "
            f"email={self.email_work!r} active={self.is_active}>"
        )
