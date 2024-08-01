from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

from hatm.domain.models import JuzStatus


@dataclass(frozen=True)
class HatmResponse(BaseModel):
    creator_id: str
    title: str
    description: str
    is_public: bool
    is_completed: bool
    is_published: bool
    created_at: datetime
    deadline: datetime


@dataclass(frozen=True)
class JuzResponse(BaseModel):
    hatm_id: str
    user_id: str
    juz_number: int
    status: JuzStatus
    deadline: datetime
