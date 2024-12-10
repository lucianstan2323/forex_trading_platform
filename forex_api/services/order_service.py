from forex_api.models.order_model import Order
from forex_api.database import SessionLocal
from uuid import uuid4

class OrderService:
    @staticmethod
    def get_all_orders():
        with SessionLocal() as db:
            return db.query(Order).all()

    @staticmethod
    def get_order(order_id: str):
        """
        Retrieve an order from the database by its ID.
        """
        with SessionLocal() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            return order

    @staticmethod
    def create_order(order_data):
        new_order = Order(
            id=str(uuid4()),
            stoks=order_data.stoks,
            quantity=order_data.quantity,
            status="pending"
        )
        with SessionLocal() as db:
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
        return new_order

    @staticmethod
    def cancel_order(order_id: str):
        with SessionLocal() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return False
            order.status = "canceled"
            db.commit()
            return True
