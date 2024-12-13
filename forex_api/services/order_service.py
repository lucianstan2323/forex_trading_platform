from forex_api.models.order_model import Order
from forex_api.schemas.order_schema import OrderResponse
from forex_api.database import async_session
from uuid import uuid4
from datetime import datetime
import asyncio
import random
from sqlalchemy.future import select
from forex_api.services.websocket_handler import WebSocketHandler

class OrderService:
    
    async def get_all_orders():
        async with async_session() as db:
            result = await db.execute(select(Order))
            orders = result.scalars().all()
            if not orders:
                return []
            return [OrderResponse.from_orm(order) for order in orders]

    async def get_order(order_id: str):
        """
        Retrieve an order from the database by its ID.
        """
        async with async_session() as db:
            result = await db.execute(select(Order).where(Order.id == order_id))
            return result.scalar_one_or_none()

    async def create_order(order_data):
        new_order = Order(
            id=str(uuid4()),
            stoks=order_data.stoks,
            quantity=order_data.quantity,
            status="pending",
            created_timestamp=datetime.utcnow()
        )

        async with async_session() as db:
            async with db.begin():  # Ensures transactional integrity
                db.add(new_order)
                
            await db.commit()  # Commit the new order
            await db.refresh(new_order) 
                    
        await WebSocketHandler.broadcast_order_status(new_order.id, "pending")

        return OrderResponse.from_orm(new_order)

    async def update_order_status_to_executed(order_id: str):
        delay = random.uniform(3.0, 7.0)
        await asyncio.sleep(delay)  # Simulate execution time

        async with async_session() as db:
            async with db.begin():
                result = await db.execute(select(Order).where(Order.id == order_id))
                order = result.scalar_one_or_none()
                if order:
                    order.status = "executed"
                    order.executed_timestamp = datetime.utcnow()

            await db.commit()
            await db.refresh(order) 

            await WebSocketHandler.broadcast_order_status(order_id, "executed")

            return OrderResponse.from_orm(order)
    
    async def cancel_order(order_id: str):
        async with async_session() as db:
            async with db.begin():
                result = await db.execute(select(Order).where(Order.id == order_id))
                order = result.scalar_one_or_none()
                if not order:
                    return False
                order.status = "canceled"
            await db.commit()

            await WebSocketHandler.broadcast_order_status(order_id, "canceled")
            
        return True
