from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrderStatusHistoryBase(BaseModel):
    order_id: int
    previous_status: str
    new_status: str
    changed_by: int


class OrderStatusHistoryCreate(OrderStatusHistoryBase):
    created_at: datetime


class OrderStatusHistoryOut(OrderStatusHistoryBase):
    order_status_history_id: int
    created_at: datetime
    changed_by_nickname: Optional[str] = None

    model_config = {"from_attributes": True}


OrderStatusHistoryBase.model_rebuild()
OrderStatusHistoryCreate.model_rebuild()
OrderStatusHistoryOut.model_rebuild()