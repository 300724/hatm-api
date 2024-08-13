from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class JuzBase(BaseModel):
    id: UUID4
    hatm_id: UUID4
    juz_number: int
    status: str
    type: str
    deadline: Optional[datetime]
    user_id: Optional[UUID4]


class HatmBase(BaseModel):
    title: str
    description: str
    is_public: bool = True
    deadline: datetime


class HatmCreate(HatmBase):
    pass  # Inherits all fields from HatmBase


class HatmGetResponse(HatmBase):
    id: UUID4
    description: str
    juzs: List[JuzBase]


class JuzTakeRequest(BaseModel):
    ids: List[UUID4]
    days: int


class JuzTakeResponse(BaseModel):
    already_taken: List[int]
    successfully_taken: List[int]
    unsuccessfully_taken: List[int]
    deadline: datetime
