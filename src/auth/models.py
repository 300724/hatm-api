from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUIDType,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Corrected relationship to Hatm
    hatms = relationship("Hatm", back_populates="creator")
    juzs = relationship("Juz", back_populates="user")