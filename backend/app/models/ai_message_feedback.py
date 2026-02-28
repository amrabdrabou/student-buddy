from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_message import AiMessage
    from app.models.user import User
    from app.models.ai_conversation import AiConversation


class AiMessageFeedback(Base):
    __tablename__ = "ai_message_feedback"

    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_messages.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_conversations.id"), nullable=False)
    feedback_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_helpful: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_accurate: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    feedback_categories: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reported_issue: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    message: Mapped["AiMessage"] = relationship("AiMessage", back_populates="feedback")
    user: Mapped["User"] = relationship("User", back_populates="ai_message_feedback")
    conversation: Mapped["AiConversation"] = relationship("AiConversation", back_populates="feedback")
