
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class NumberSeries(Base):
    __tablename__ = "number_series"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    pattern: Mapped[str] = mapped_column(String(50))
    current_no: Mapped[int] = mapped_column(Integer, default=0)
    year: Mapped[int] = mapped_column(Integer)
