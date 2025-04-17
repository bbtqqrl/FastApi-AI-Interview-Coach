from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from core.models.base import Base

class User(Base):

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = mapped_column(String, nullable=True)
    last_name = mapped_column(String, nullable=True)
    email = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash = mapped_column(String, nullable=False)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
