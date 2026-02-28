from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User


class AiUsageStats(Base):
    __tablename__ = "ai_usage_stats"
    __table_args__ = (UniqueConstraint("user_id", "stat_date"),)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    stat_date: Mapped[date] = mapped_column(Date, nullable=False)
    stat_period: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    conversations_started: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversations_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_messages_sent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens_consumed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_cost_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    flashcards_generated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    summaries_generated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_conversation_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="ai_usage_stats")
