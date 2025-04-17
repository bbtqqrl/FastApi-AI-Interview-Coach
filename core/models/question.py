from datetime import datetime
from uuid import uuid4
from sqlalchemy import ForeignKey, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from core.models.base import Base


class Question(Base):

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_text = mapped_column(Text, nullable=False)
    answer_text = mapped_column(Text, nullable=True)
    ai_feedback = mapped_column(Text, nullable=True)
    score = mapped_column(Integer, nullable=True)

    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="questions")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
