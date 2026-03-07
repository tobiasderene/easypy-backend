from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class OAuthAccountBase(BaseModel):
    user_id: int
    provider: str
    provider_user_id: Optional[str] = None
    email: EmailStr
    name: str


class OAuthAccountCreate(OAuthAccountBase):
    password: Optional[str] = None
    password_hash: Optional[str] = None
    created_at: datetime


class OAuthAccountUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    password_hash: Optional[str] = None
    provider_user_id: Optional[str] = None


class OAuthAccountOut(OAuthAccountBase):
    oauth_account_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


OAuthAccountBase.model_rebuild()
OAuthAccountCreate.model_rebuild()
OAuthAccountUpdate.model_rebuild()
OAuthAccountOut.model_rebuild()


class LocalRegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    user_role: str


class LocalLoginSchema(BaseModel):
    email: EmailStr
    password: str


LocalRegisterSchema.model_rebuild()
LocalLoginSchema.model_rebuild()