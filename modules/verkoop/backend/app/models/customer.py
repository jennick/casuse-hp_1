
from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class CustomerShadow(Base):
    __tablename__ = "customer_shadow"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    website_customer_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id", ondelete="SET NULL"), nullable=True)

class CustomerAssignment(Base):
    __tablename__ = "customer_assignments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_shadow.id", ondelete="CASCADE"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="active")
    auto_assigned: Mapped[bool] = mapped_column(Boolean, default=False)
