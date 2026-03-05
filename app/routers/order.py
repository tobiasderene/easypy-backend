from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderOut
from app.schemas.order_status_history import OrderStatusHistoryCreate, OrderStatusHistoryOut
from app.crud import order as crud_order
from app.crud import order_status_history as crud_history

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderOut])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.get_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_order


@router.get("/buyer/{buyer_id}", response_model=List[OrderOut])
def get_orders_by_buyer(buyer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.get_orders_by_buyer(db, buyer_id, skip=skip, limit=limit)


@router.get("/supplier/{supplier_id}", response_model=List[OrderOut])
def get_orders_by_supplier(supplier_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.get_orders_by_supplier(db, supplier_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[OrderOut])
def get_orders_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.get_orders_by_status(db, status, skip=skip, limit=limit)


@router.get("/{order_id}/history", response_model=List[OrderStatusHistoryOut])
def get_order_history(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return crud_history.get_status_history_by_order(db, order_id)


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order)


@router.patch("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud_order.update_order(db, order_id, order)
    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_order


@router.delete("/{order_id}", response_model=OrderOut)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.delete_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_order