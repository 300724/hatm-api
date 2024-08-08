import json
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func,Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import Base

class Hatm(Base):
    __tablename__ = "hatms"

    id = Column(UUIDType(as_uuid=True), primary_key=True, index=True, default=uuid4(), unique=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime, nullable=False)
    juzs = Column(JSON, nullable=False, default=lambda: json.dumps([
        {
            "id": x + 1,
            "name": f"Juz {x + 1}",
            "start_page": x * 20 + 1,
            "end_page": (x + 1) * 20,
            "is_completed": False,
            "is_dua": (x == 30),
            "user_id": None
        }
        for x in range(31)
    ]))

    creator_id = Column(UUIDType(as_uuid=True), ForeignKey('users.id'))

    creator = relationship("User", back_populates="hatms")
