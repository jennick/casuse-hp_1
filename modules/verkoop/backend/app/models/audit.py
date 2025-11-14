
from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    when: Mapped[str] = mapped_column(DateTime)
    actor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    action: Mapped[str] = mapped_column(String(50))
    entity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[dict] = mapped_column(
    JSONB, nullable=False, server_default=text("'{}'::jsonb")
)

