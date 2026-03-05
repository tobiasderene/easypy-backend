from __future__ import annotations
from pydantic import BaseModel


class LogisticsBase(BaseModel):
    pass


class LogisticsCreate(LogisticsBase):
    logistic_id: int


class LogisticsOut(LogisticsBase):
    logistic_id: int

    model_config = {"from_attributes": True}


LogisticsBase.model_rebuild()
LogisticsCreate.model_rebuild()
LogisticsOut.model_rebuild()