from sqlalchemy.orm import Session
from app.db.models import Order, OrderForBankMovement
from app.schemas.order import OrderCreate, OrderUpdate


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def get_orders_by_buyer(db: Session, buyer_id: int, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(Order.buyer_id == buyer_id).offset(skip).limit(limit).all()


def get_orders_by_supplier(db: Session, supplier_id: int, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(Order.supplier_id == supplier_id).offset(skip).limit(limit).all()


def get_orders_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(Order.status == status).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if not db_order:
        return None
    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order