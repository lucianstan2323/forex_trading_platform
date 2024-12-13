from sqlalchemy import Column, String, Float, DateTime
from forex_api.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    stoks = Column(String, index=True)
    quantity = Column(Float)
    status = Column(String, default="pending", nullable=True)
    created_timestamp = Column(DateTime, default=datetime.utcnow, nullable=True)
    executed_timestamp = Column(DateTime, nullable=True)
