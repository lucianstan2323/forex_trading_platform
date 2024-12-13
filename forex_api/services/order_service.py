from forex_api.models.order_model import Order
from forex_api.schemas.order_schema import OrderResponse
from forex_api.database import async_session
from uuid import uuid4
from datetime import datetime
import asyncio
import random
from sqlalchemy.future import select

class OrderService:
    
    async def get_all_orders():
        async with async_session() as db:
            result = await db.execute(select(Order))
            return result.scalars().all()

    
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
            
            # Simulate a short delay and update the status to EXECUTED
            delay = random.uniform(3.0, 7.0)
            await asyncio.sleep(delay)

        async with async_session() as db:
            async with db.begin():
                result = await db.execute(select(Order).where(Order.id == new_order.id))
                order = result.scalar_one_or_none()
                order.status = "executed"
                order.executed_timestamp = datetime.utcnow()

            await db.commit()  # Commit the new order
            await db.refresh(order) 
                    
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
        return True
