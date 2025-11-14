
from sqlalchemy import Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_no: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customer_shadow.id", ondelete="SET NULL"))
    seller_id: Mapped[int | None] = mapped_column(ForeignKey("sellers.id", ondelete="SET NULL"))
    seller_book_no: Mapped[str | None] = mapped_column(String(30), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="MXN")
    subtotal: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    vat: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    total: Mapped[float] = mapped_column(Numeric(14,2), default=0)
    status: Mapped[str] = mapped_column(String(20), default="created")

class SalesOrderLine(Base):
    __tablename__ = "sales_order_lines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("sales_orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product_catalog.id", ondelete="RESTRICT"))
    qty: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Numeric(12,2))
    discount_percent: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    line_total: Mapped[float] = mapped_column(Numeric(14,2))
