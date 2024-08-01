from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

from hatm.domain.models import JuzStatus


@dataclass(frozen=True)
class CreateHatmRequest(BaseModel):
    creator_id: str
    title: str
    description: str
    is_public: bool
    deadline: datetime


@dataclass(frozen=True)
class UpdateHatmRequest(BaseModel):
    title: str = None
    description: str = None
    is_public: bool = None
    is_completed: bool = None
    is_published: bool = None
    deadline: datetime = None


@dataclass(frozen=True)
class CreateJuzRequest(BaseModel):
    user_id: str
    juz_number: int
    status: JuzStatus
    deadline: datetime


@dataclass(frozen=True)
class UpdateJuzRequest(BaseModel):
    status: JuzStatus = None
    deadline: datetime = None
