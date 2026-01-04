
from sqlalchemy import Column, String
from database import Base

class CustomerModuleRelation(Base):
    __tablename__ = "customer_module_relations"

    id = Column(String, primary_key=True)
    customer_id = Column(String, index=True, nullable=False)
    module = Column(String, nullable=False)
