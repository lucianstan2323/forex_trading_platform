from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class OrderBase(BaseModel):
    stoks: str
    quantity: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: str
    quantity: float
    stoks: str
    status: Literal["pending", "executed", "canceled"]
    created_timestamp: Optional[datetime]
    executed_timestamp: Optional[datetime]

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    code: int
    message: str


