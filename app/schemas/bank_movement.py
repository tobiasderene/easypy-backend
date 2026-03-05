from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class BankMovementBase(BaseModel):
    bank_movement_type: str
    amount: Decimal
    reference_number: str
    status: str
    withdrawls_id: Optional[int] = None


class BankMovementCreate(BankMovementBase):
    created_at: datetime
    order_ids: List[int] = []


class BankMovementUpdate(BaseModel):
    status: Optional[str] = None
    reference_number: Optional[str] = None


class BankMovementOut(BankMovementBase):
    bank_movement_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class BankMovementDetails(BankMovementOut):
    order_ids: List[int] = []

    model_config = {"from_attributes": True}


BankMovementBase.model_rebuild()
BankMovementCreate.model_rebuild()
BankMovementUpdate.model_rebuild()
BankMovementOut.model_rebuild()
BankMovementDetails.model_rebuild()