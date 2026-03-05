from __future__ import annotations
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class WalletBase(BaseModel):
    user_id: int
    balance_available: Decimal
    balance_pending: Decimal


class WalletCreate(WalletBase):
    created_at: datetime
    updated_at: datetime


class WalletUpdate(BaseModel):
    balance_available: Optional[Decimal] = None
    balance_pending: Optional[Decimal] = None
    updated_at: Optional[datetime] = None


class WalletOut(WalletBase):
    wallet_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


WalletBase.model_rebuild()
WalletCreate.model_rebuild()
WalletUpdate.model_rebuild()
WalletOut.model_rebuild()