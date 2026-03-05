from __future__ import annotations
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class WithdrawalBase(BaseModel):
    wallet_id: int
    amount: Decimal
    status: str
    bank_account_address: str
    bank_name: str


class WithdrawalCreate(WithdrawalBase):
    created_at: datetime
    processed_at: datetime


class WithdrawalUpdate(BaseModel):
    status: Optional[str] = None
    processed_at: Optional[datetime] = None


class WithdrawalOut(WithdrawalBase):
    withdrawls_id: int
    created_at: datetime
    processed_at: datetime

    model_config = {"from_attributes": True}


WithdrawalBase.model_rebuild()
WithdrawalCreate.model_rebuild()
WithdrawalUpdate.model_rebuild()
WithdrawalOut.model_rebuild()