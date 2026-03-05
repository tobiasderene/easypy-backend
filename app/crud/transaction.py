from sqlalchemy.orm import Session
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id_transaction == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_transactions_by_wallet(db: Session, wallet_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(Transaction.wallet_id == wallet_id).offset(skip).limit(limit).all()


def get_transactions_by_order(db: Session, order_id: int):
    return db.query(Transaction).filter(Transaction.order_id == order_id).all()


def get_transactions_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(Transaction.transaction_status == status).offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = db.query(Transaction).filter(Transaction.id_transaction == transaction_id).first()
    if not db_transaction:
        return None
    for field, value in transaction.model_dump(exclude_unset=True).items():
        setattr(db_transaction, field, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction