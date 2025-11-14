
from sqlalchemy import Integer, String, Numeric, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

class PaymentIntent(Base):
    __tablename__ = "payment_intents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("sales_orders.id", ondelete="CASCADE"))
    provider: Mapped[str] = mapped_column(String(50))
    intent_id: Mapped[str] = mapped_column(String(100), unique=True)
    amount: Mapped[float] = mapped_column(Numeric(14,2))
    currency: Mapped[str] = mapped_column(String(10), default="MXN")
    status: Mapped[str] = mapped_column(String(20), default="requires_payment_method")
    payment_metadata: Mapped[dict | None] = mapped_column(
    "metadata", JSONB, nullable=True, server_default=text("'{}'::jsonb")
)

