from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    __table_args__ = (UniqueConstraint("user_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    preferred_ai_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    preferred_temperature: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    preferred_max_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    conversation_style: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    explanation_depth: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    preferred_language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    enable_socratic_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    enable_step_by_step: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    enable_rag_context: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_context_messages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="preferences")
