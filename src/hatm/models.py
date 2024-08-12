from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Juz(Base):
    __tablename__ = "juzs"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    index = Column(Integer, nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"))
    hatm_id = Column(String, ForeignKey("hatms.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    hatm = relationship("Juz", back_populates="hatms")


class Hatm(Base):
    __tablename__ = "hatms"

    id = Column(
        String,
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
    creator_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    creator = relationship("User", back_populates="hatms")
    juzs = relationship("Juz", back_populates="hatms")
