from datetime import datetime

from pydantic import BaseModel

from hatm.domain.models import JuzStatus


class CreateHatmRequest(BaseModel):
    creator_id: str
    title: str
    description: str
    is_public: bool
    deadline: datetime


class UpdateHatmRequest(BaseModel):
    title: str = None
    description: str = None
    is_public: bool = None
    is_completed: bool = None
    is_published: bool = None
    deadline: datetime = None


class CreateJuzRequest(BaseModel):
    user_id: str
    juz_number: int
    status: JuzStatus
    deadline: datetime


class UpdateJuzRequest(BaseModel):
    status: JuzStatus = None
    deadline: datetime = None
