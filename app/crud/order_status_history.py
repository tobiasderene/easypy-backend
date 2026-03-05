from sqlalchemy.orm import Session
from app.db.models import OrderStatusHistory
from app.schemas.order_status_history import OrderStatusHistoryCreate


def get_status_history_by_order(db: Session, order_id: int):
    return db.query(OrderStatusHistory).filter(OrderStatusHistory.order_id == order_id).all()


def create_order_status_history(db: Session, history: OrderStatusHistoryCreate):
    db_history = OrderStatusHistory(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history