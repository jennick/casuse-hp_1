# verkoop/backend/app/models/domain_event.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func, text as sa_text

from app.db.base_class import Base


class DomainEvent(Base):
    """Eenvoudige domain-event tabel voor auditable business events.

    Dit is geen volledige outbox-implementatie, maar laat toe om later
    events asynchroon naar andere systemen te sturen.
    """

    __tablename__ = "domain_events"

    id: int = Column(Integer, primary_key=True, index=True)
    event_type: str = Column(String(100), nullable=False)
    entity_type: str = Column(String(50), nullable=False)
    entity_id: str | None = Column(String(100), nullable=True)

    # JSON payload met extra gegevens (bv. customer_id, seller_id, enz.)
    payload_json = Column(
        JSONB,
        nullable=False,
        server_default=sa_text("'{}'::jsonb"),
    )

    created_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:  # pragma: no cover - enkel voor debugging
        return (
            f"<DomainEvent id={self.id} type={self.event_type!r} "
            f"entity_type={self.entity_type!r} entity_id={self.entity_id!r}>"
        )
