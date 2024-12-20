from fastapi import APIRouter, HTTPException
from forex_api.schemas.order_schema import OrderCreate, OrderResponse
from forex_api.services.order_service import OrderService

router = APIRouter()

@router.get("/", response_model=list[OrderResponse])
async def get_orders():
    return OrderService.get_all_orders()

@router.get("/{orderId}", response_model=OrderResponse)
async def get_order_route(orderId: str):
    """
    Retrieve a specific order by its ID.
    """
    order = OrderService.get_order(orderId)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse, status_code=201)
async def place_order(order: OrderCreate):
    
    order = OrderService.create_order(order)
        
    if not order:
        raise HTTPException(status_code=400, detail="Invalid input")
    return order
 
@router.delete("/{order_id}", status_code=204)
async def cancel_order(order_id: str):
    if not OrderService.cancel_order(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
