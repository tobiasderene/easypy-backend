from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ProductBase(BaseModel):
    product_name: str
    product_base_cost: Decimal
    product_sku: str
    product_status: str
    product_description: str
    user_id: int
    product_category: str
    product_discount: Decimal


class ProductCreate(ProductBase):
    created_at: datetime


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_base_cost: Optional[Decimal] = None
    product_sku: Optional[str] = None
    product_status: Optional[str] = None
    product_description: Optional[str] = None
    product_category: Optional[str] = None
    product_discount: Optional[Decimal] = None


class ProductOut(ProductBase):
    product_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductDetails(ProductOut):
    images: List[str] = []
    primary_image: Optional[str] = None

    model_config = {"from_attributes": True}


ProductBase.model_rebuild()
ProductCreate.model_rebuild()
ProductUpdate.model_rebuild()
ProductOut.model_rebuild()
ProductDetails.model_rebuild()