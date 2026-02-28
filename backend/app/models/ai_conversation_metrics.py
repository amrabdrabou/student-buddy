from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_conversation import AiConversation
    from app.models.user import User
    from app.models.study_subject import StudySubject


class AiConversationMetrics(Base):
    __tablename__ = "ai_conversation_metrics"
    __table_args__ = (UniqueConstraint("conversation_id"),)

    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_conversations.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    user_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assistant_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_tokens_per_message: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    avg_response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    thread_depth_max: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversation_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    primary_subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    detected_topics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    conversation: Mapped["AiConversation"] = relationship("AiConversation", back_populates="metrics")
    user: Mapped["User"] = relationship("User", back_populates="ai_conversation_metrics")
    primary_subject: Mapped[Optional["StudySubject"]] = relationship(
        "StudySubject", back_populates="conversation_metrics", foreign_keys=[primary_subject_id]
    )
