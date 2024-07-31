from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


@dataclass(frozen=True)
class Hatm(BaseModel):
    creator_id: str
    title: str
    description: str
    is_public: bool
    is_completed: bool
    is_published: bool
    created_at: datetime
    deadline: datetime


@dataclass(frozen=True)
class JuzStatus(Enum):
    FREE = "free"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Juz(BaseModel):
    hatm_id: str
    user_id: str
    juz_number: int
    status: JuzStatus
    deadline: datetime

    def __post_init__(self) -> None:
        if self.juz_number < 1 or self.juz_number > 31:
            raise ValueError("Juz number must be in range [1, 31] (31 is Du'a)")
