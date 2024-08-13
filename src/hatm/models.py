from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import event
from sqlalchemy.orm import Session

from database import Base


class JusStatusEnum(str, Enum):
    completed = "completed"
    in_progress = "in_progress"
    free = "free"


class Juz(Base):
    __tablename__ = "juzs"

    id = Column(UUIDType, primary_key=True, index=True, unique=True, nullable=False)
    index = Column(Integer, nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(UUIDType, ForeignKey("users.id"))
    hatm_id = Column(UUIDType(as_uuid=True), ForeignKey("hatms.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deadline = Column(DateTime, nullable=True)

    # Relationships to Hatm and User
    hatm = relationship("Hatm", back_populates="juzs")
    user = relationship("User", back_populates="juzs")


class Hatm(Base):
    __tablename__ = "hatms"

    id = Column(
        UUIDType,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime, nullable=False)
    creator_id = Column(UUIDType(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Corrected relationship to User
    creator = relationship("User", back_populates="hatms")
    juzs = relationship("Juz", back_populates="hatm")