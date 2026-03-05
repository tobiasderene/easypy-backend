from sqlalchemy.orm import Session
from app.db.models import BankMovement, OrderForBankMovement
from app.schemas.bank_movement import BankMovementCreate, BankMovementUpdate


def get_bank_movement(db: Session, bank_movement_id: int):
    return db.query(BankMovement).filter(BankMovement.bank_movement_id == bank_movement_id).first()


def get_bank_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BankMovement).offset(skip).limit(limit).all()


def get_bank_movements_by_withdrawal(db: Session, withdrawal_id: int):
    return db.query(BankMovement).filter(BankMovement.withdrawls_id == withdrawal_id).all()


def get_bank_movements_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    return db.query(BankMovement).filter(BankMovement.status == status).offset(skip).limit(limit).all()


def create_bank_movement(db: Session, bank_movement: BankMovementCreate):
    data = bank_movement.model_dump()
    order_ids = data.pop("order_ids", [])

    db_bank_movement = BankMovement(**data)
    db.add(db_bank_movement)
    db.flush()

    for order_id in order_ids:
        link = OrderForBankMovement(
            bank_movement_id=db_bank_movement.bank_movement_id,
            order_id=order_id
        )
        db.add(link)

    db.commit()
    db.refresh(db_bank_movement)
    return db_bank_movement


def update_bank_movement(db: Session, bank_movement_id: int, bank_movement: BankMovementUpdate):
    db_bank_movement = db.query(BankMovement).filter(BankMovement.bank_movement_id == bank_movement_id).first()
    if not db_bank_movement:
        return None
    for field, value in bank_movement.model_dump(exclude_unset=True).items():
        setattr(db_bank_movement, field, value)
    db.commit()
    db.refresh(db_bank_movement)
    return db_bank_movement