from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func,Boolean
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUIDType(as_uuid=True), primary_key=True, index=True, default=uuid4(), unique=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    hatms = relationship("Hatm", back_populates="users")