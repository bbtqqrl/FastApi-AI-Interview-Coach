from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class User(Base):

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = mapped_column(String(32), nullable=True)
    email = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow())
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return str(self)

