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