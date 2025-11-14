
from typing import Optional, List, Dict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

from sqlalchemy import Integer, String, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Quote(Base):
    __tablename__ = "quotes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_no: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customer_shadow.id", ondelete="SET NULL"), nullable=True)
    seller_id: Mapped[int | None] = mapped_column(ForeignKey("sellers.id", ondelete="SET NULL"), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="MXN")
    subtotal: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    vat: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    total: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    status: Mapped[str] = mapped_column(String(20), default="draft")

class QuoteLine(Base):
    __tablename__ = "quote_lines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_id: Mapped[int] = mapped_column(ForeignKey("quotes.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product_catalog.id", ondelete="RESTRICT"))
    qty: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Numeric(12,2))
    discount_percent: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    line_total: Mapped[float] = mapped_column(Numeric(14,2))

class FeasibilityCheck(Base):
    __tablename__ = "feasibility_checks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_id: Mapped[int] = mapped_column(ForeignKey("quotes.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    attachments: Mapped[Optional[List[Dict]]] = mapped_column(
    JSONB, nullable=True, server_default=text("'[]'::jsonb")
)

