from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.withdrawal import WithdrawalCreate, WithdrawalUpdate, WithdrawalOut
from app.crud import withdrawal as crud_withdrawal
from app.dependencies import get_current_user

router = APIRouter(prefix="/withdrawals", tags=["Withdrawals"])


@router.get("/", response_model=List[WithdrawalOut])
def get_withdrawals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud_withdrawal.get_withdrawals(db, skip=skip, limit=limit)


@router.get("/wallet/{wallet_id}", response_model=List[WithdrawalOut])
def get_withdrawals_by_wallet(
    wallet_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud_withdrawal.get_withdrawals_by_wallet(db, wallet_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[WithdrawalOut])
def get_withdrawals_by_status(
    status: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud_withdrawal.get_withdrawals_by_status(db, status, skip=skip, limit=limit)


@router.get("/{withdrawal_id}", response_model=WithdrawalOut)
def get_withdrawal(
    withdrawal_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_withdrawal = crud_withdrawal.get_withdrawal(db, withdrawal_id)
    if not db_withdrawal:
        raise HTTPException(status_code=404, detail="Retiro no encontrado")
    return db_withdrawal


@router.post("/", response_model=WithdrawalOut, status_code=201)
def create_withdrawal(
    withdrawal: WithdrawalCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud_withdrawal.create_withdrawal(db, withdrawal)


@router.patch("/{withdrawal_id}", response_model=WithdrawalOut)
def update_withdrawal(
    withdrawal_id: int,
    withdrawal: WithdrawalUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_withdrawal = crud_withdrawal.update_withdrawal(db, withdrawal_id, withdrawal)
    if not db_withdrawal:
        raise HTTPException(status_code=404, detail="Retiro no encontrado")
    return db_withdrawal