
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Region(Base):
    __tablename__ = "regions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    cities: Mapped[list["City"]] = relationship(back_populates="region")

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"))
    region: Mapped[Region] = relationship(back_populates="cities")
