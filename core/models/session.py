from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class Session(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    topic_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    topic = relationship("Topic")

    topic_title: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")

    responses = relationship("UserResponse", back_populates="session", cascade="all, delete-orphan")

    overall_score: Mapped[int] = mapped_column(Integer, nullable=True) 
    overall_feedback: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
