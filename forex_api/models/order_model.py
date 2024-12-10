from sqlalchemy import Column, String, Float
from forex_api.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    stoks = Column(String, index=True)
    quantity = Column(Float)
    status = Column(String, default="pending")
