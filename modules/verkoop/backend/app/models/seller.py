
from sqlalchemy import Integer, String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Seller(Base):
    __tablename__ = "sellers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    max_discount_percent: Mapped[float] = mapped_column(Numeric(5,2))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
