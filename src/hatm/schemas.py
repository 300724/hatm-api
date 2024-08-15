from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel


@dataclass(frozen=True)
class JuzBase(BaseModel):
    id: UUID4
    hatm_id: UUID4
    juz_number: int
    status: str
    type: str
    deadline: Optional[datetime]
    user_id: Optional[UUID4]


@dataclass(frozen=True)
class HatmBase(BaseModel):
    title: str
    description: str
    is_public: bool = True
    deadline: datetime


@dataclass(frozen=True)
class HatmCreate(HatmBase):
    pass  # Inherits all fields from HatmBase


@dataclass(frozen=True)
class HatmGetResponse(HatmBase):
    id: UUID4
    description: str
    juzs: List[JuzBase]


@dataclass(frozen=True)
class JuzTakeRequest(BaseModel):
    ids: List[UUID4]
    days: int


@dataclass(frozen=True)
class JuzTakeResponse(BaseModel):
    already_taken: List[int]
    successfully_taken: List[int]
    unsuccessfully_taken: List[int]
    deadline: datetime
