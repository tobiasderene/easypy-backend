from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.wallet import WalletCreate, WalletUpdate, WalletOut
from app.crud import wallet as crud_wallet

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.get("/{wallet_id}", response_model=WalletOut)
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    db_wallet = crud_wallet.get_wallet(db, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet no encontrada")
    return db_wallet


@router.get("/user/{user_id}", response_model=WalletOut)
def get_wallet_by_user(user_id: int, db: Session = Depends(get_db)):
    db_wallet = crud_wallet.get_wallet_by_user(db, user_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet no encontrada para este usuario")
    return db_wallet


@router.post("/", response_model=WalletOut, status_code=201)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    existing = crud_wallet.get_wallet_by_user(db, wallet.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Este usuario ya tiene una wallet")
    return crud_wallet.create_wallet(db, wallet)


@router.patch("/{wallet_id}", response_model=WalletOut)
def update_wallet(wallet_id: int, wallet: WalletUpdate, db: Session = Depends(get_db)):
    db_wallet = crud_wallet.update_wallet(db, wallet_id, wallet)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet no encontrada")
    return db_wallet