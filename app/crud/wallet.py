from sqlalchemy.orm import Session
from app.db.models import Wallet
from app.schemas.wallet import WalletCreate, WalletUpdate


def get_wallet(db: Session, wallet_id: int):
    return db.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()


def get_wallet_by_user(db: Session, user_id: int):
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()


def create_wallet(db: Session, wallet: WalletCreate):
    db_wallet = Wallet(**wallet.model_dump())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


def update_wallet(db: Session, wallet_id: int, wallet: WalletUpdate):
    db_wallet = db.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()
    if not db_wallet:
        return None
    for field, value in wallet.model_dump(exclude_unset=True).items():
        setattr(db_wallet, field, value)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet