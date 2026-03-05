from sqlalchemy.orm import Session
from app.db.models import Withdrawal
from app.schemas.withdrawal import WithdrawalCreate, WithdrawalUpdate


def get_withdrawal(db: Session, withdrawal_id: int):
    return db.query(Withdrawal).filter(Withdrawal.withdrawls_id == withdrawal_id).first()


def get_withdrawals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Withdrawal).offset(skip).limit(limit).all()


def get_withdrawals_by_wallet(db: Session, wallet_id: int, skip: int = 0, limit: int = 100):
    return db.query(Withdrawal).filter(Withdrawal.wallet_id == wallet_id).offset(skip).limit(limit).all()


def get_withdrawals_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(Withdrawal).filter(Withdrawal.status == status).offset(skip).limit(limit).all()


def create_withdrawal(db: Session, withdrawal: WithdrawalCreate):
    db_withdrawal = Withdrawal(**withdrawal.model_dump())
    db.add(db_withdrawal)
    db.commit()
    db.refresh(db_withdrawal)
    return db_withdrawal


def update_withdrawal(db: Session, withdrawal_id: int, withdrawal: WithdrawalUpdate):
    db_withdrawal = db.query(Withdrawal).filter(Withdrawal.withdrawls_id == withdrawal_id).first()
    if not db_withdrawal:
        return None
    for field, value in withdrawal.model_dump(exclude_unset=True).items():
        setattr(db_withdrawal, field, value)
    db.commit()
    db.refresh(db_withdrawal)
    return db_withdrawal