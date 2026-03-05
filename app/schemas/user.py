from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    user_nickname: str
    user_role: str
    user_status: str
    user_description: str


class UserCreate(UserBase):
    created_at: datetime


class UserUpdate(BaseModel):
    user_nickname: Optional[str] = None
    user_role: Optional[str] = None
    user_status: Optional[str] = None
    user_description: Optional[str] = None


class UserOut(UserBase):
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


UserBase.model_rebuild()
UserCreate.model_rebuild()
UserUpdate.model_rebuild()
UserOut.model_rebuild()