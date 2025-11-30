# verkoop/backend/app/db/base.py

# Import all models here so Alembic / metadata can see them.
from app.db.base_class import Base  # noqa
from app.models.seller import Seller  # noqa
from app.models.customer import CustomerShadow, CustomerSellerAssignment  # noqa
from app.models.domain_event import DomainEvent  # noqa
