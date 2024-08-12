from datetime import datetime

from pydantic import BaseModel


class Juz(BaseModel):
    id: str
    hatm_id: int
    juz_number: int
    status: str
    type: str
    deadline: datetime
    user_id: int


class TakeJuz(BaseModel):
    ids: list[str]
    days: int


class TakeJuzResponse(BaseModel):
    already_taken: list[str]
    successfully_taken: list[str]
    unseccesfully_taken: list[str]
    deadline: datetime


class Message(BaseModel):
    message: str
