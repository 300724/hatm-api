from datetime import datetime

from pydantic import BaseModel

from juz.schemas import Juz


class HatmCreate(BaseModel):
    is_public: bool
    title: str
    description: str
    deadline: datetime


class HatmGet(HatmCreate):
    id: str
    is_public: bool
    title: str
    description: str
    juzs: list[Juz]
