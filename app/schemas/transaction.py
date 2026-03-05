from __future__ import annotations
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class TransactionBase(BaseModel):
    wallet_id: int
    order_id: Optional[int] = None
    transaction_category: str
    transaction_direction: str
    transaction_amount: Decimal
    transaction_status: str


class TransactionCreate(TransactionBase):
    created_at: datetime


class TransactionUpdate(BaseModel):
    transaction_status: Optional[str] = None


class TransactionOut(TransactionBase):
    id_transaction: int
    created_at: datetime

    model_config = {"from_attributes": True}


TransactionBase.model_rebuild()
TransactionCreate.model_rebuild()
TransactionUpdate.model_rebuild()
TransactionOut.model_rebuild()