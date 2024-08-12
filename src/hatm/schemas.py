from datetime import datetime

from pydantic import BaseModel

from juz.schemas import Juz


class HatmCreateDto(BaseModel):
    is_public: bool
    title: str
    description: str
    deadline: datetime


class HatmGetDto(BaseModel):
    id: str
    is_public: bool
    title: str
    description: str
    juzs: list[Juz]
