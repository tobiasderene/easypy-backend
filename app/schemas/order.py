from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.order_status_history import OrderStatusHistoryOut


class OrderBase(BaseModel):
    buyer_id: int
    supplier_id: int
    logistic_id: int
    product_id: int
    final_price: Decimal
    supplier_cost: Decimal
    logistic_cost: Decimal
    platform_fee: Decimal
    buyer_profit: Decimal
    status: str


class OrderCreate(OrderBase):
    created_at: datetime
    updated_at: datetime


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    final_price: Optional[Decimal] = None
    supplier_cost: Optional[Decimal] = None
    logistic_cost: Optional[Decimal] = None
    platform_fee: Optional[Decimal] = None
    buyer_profit: Optional[Decimal] = None
    updated_at: Optional[datetime] = None


class OrderOut(OrderBase):
    order_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderDetails(OrderOut):
    buyer_nickname: Optional[str] = None
    supplier_nickname: Optional[str] = None
    product_name: Optional[str] = None
    status_history: List[OrderStatusHistoryOut] = []

    model_config = {"from_attributes": True}


OrderBase.model_rebuild()
OrderCreate.model_rebuild()
OrderUpdate.model_rebuild()
OrderOut.model_rebuild()
OrderDetails.model_rebuild()