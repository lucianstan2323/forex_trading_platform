from pydantic import BaseModel

class OrderBase(BaseModel):
    stoks: str
    quantity: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: str
    status: str

class ErrorResponse(BaseModel):
    code: int
    message: str
