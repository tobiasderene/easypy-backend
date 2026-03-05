from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ImageBase(BaseModel):
    image_url: str
    is_primary: bool = False
    position: Optional[int] = None
    product_id: Optional[int] = None
    user_id: Optional[int] = None


class ImageCreate(ImageBase):
    created_at: datetime


class ImageUpdate(BaseModel):
    image_url: Optional[str] = None
    is_primary: Optional[bool] = None
    position: Optional[int] = None


class ImageOut(ImageBase):
    image_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


ImageBase.model_rebuild()
ImageCreate.model_rebuild()
ImageUpdate.model_rebuild()
ImageOut.model_rebuild()