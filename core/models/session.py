from datetime import datetime
from uuid import uuid4
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from core.models.base import Base


class Session(Base):

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_name = mapped_column(String, nullable=False)

    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
