from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut
from app.crud import transaction as crud_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionOut])
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_transaction.get_transactions(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.get_transaction(db, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_transaction


@router.get("/wallet/{wallet_id}", response_model=List[TransactionOut])
def get_transactions_by_wallet(wallet_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_transaction.get_transactions_by_wallet(db, wallet_id, skip=skip, limit=limit)


@router.get("/order/{order_id}", response_model=List[TransactionOut])
def get_transactions_by_order(order_id: int, db: Session = Depends(get_db)):
    return crud_transaction.get_transactions_by_order(db, order_id)


@router.post("/", response_model=TransactionOut, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud_transaction.create_transaction(db, transaction)


@router.patch("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.update_transaction(db, transaction_id, transaction)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_transaction