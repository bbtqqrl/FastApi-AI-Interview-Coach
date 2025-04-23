from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class UserResponse(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    question_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("questions.id", ondelete="SET NULL"), nullable=True)
    question = relationship("Question")

    question_text: Mapped[str] = mapped_column(Text, nullable=False)

    session_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="responses")

    answer_text: Mapped[str] = mapped_column(Text, nullable=True)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    score: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
