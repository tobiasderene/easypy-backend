from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.bank_movement import BankMovementCreate, BankMovementUpdate, BankMovementOut
from app.crud import bank_movement as crud_bank_movement

router = APIRouter(prefix="/bank-movements", tags=["Bank Movements"])


@router.get("/", response_model=List[BankMovementOut])
def get_bank_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_bank_movement.get_bank_movements(db, skip=skip, limit=limit)


@router.get("/{bank_movement_id}", response_model=BankMovementOut)
def get_bank_movement(bank_movement_id: int, db: Session = Depends(get_db)):
    db_bm = crud_bank_movement.get_bank_movement(db, bank_movement_id)
    if not db_bm:
        raise HTTPException(status_code=404, detail="Movimiento bancario no encontrado")
    return db_bm


@router.get("/withdrawal/{withdrawal_id}", response_model=List[BankMovementOut])
def get_bank_movements_by_withdrawal(withdrawal_id: int, db: Session = Depends(get_db)):
    return crud_bank_movement.get_bank_movements_by_withdrawal(db, withdrawal_id)


@router.get("/status/{status}", response_model=List[BankMovementOut])
def get_bank_movements_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_bank_movement.get_bank_movements_by_status(db, status, skip=skip, limit=limit)


@router.post("/", response_model=BankMovementOut, status_code=201)
def create_bank_movement(bank_movement: BankMovementCreate, db: Session = Depends(get_db)):
    return crud_bank_movement.create_bank_movement(db, bank_movement)


@router.patch("/{bank_movement_id}", response_model=BankMovementOut)
def update_bank_movement(bank_movement_id: int, bank_movement: BankMovementUpdate, db: Session = Depends(get_db)):
    db_bm = crud_bank_movement.update_bank_movement(db, bank_movement_id, bank_movement)
    if not db_bm:
        raise HTTPException(status_code=404, detail="Movimiento bancario no encontrado")
    return db_bm