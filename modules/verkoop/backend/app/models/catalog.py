
from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class ProductCatalog(Base):
    __tablename__ = "product_catalog"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    base_price: Mapped[float] = mapped_column(Numeric(12,2))
    vat_rate: Mapped[float] = mapped_column(Numeric(5,2))

class PriceRule(Base):
    __tablename__ = "price_rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product_catalog.id', ondelete='CASCADE'))
    min_qty: Mapped[int] = mapped_column(Integer, default=1)
    discount_percent: Mapped[float] = mapped_column(Numeric(5,2), default=0)
