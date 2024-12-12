from pydantic import BaseModel
from typing import Literal

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

class ErrorResponse(BaseModel):
    code: int
    message: str
