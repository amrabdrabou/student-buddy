from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_message import AiMessage


class AiMessageIntent(Base):
    __tablename__ = "ai_message_intents"

    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_messages.id"), nullable=False)
    intent_type: Mapped[str] = mapped_column(String, nullable=False)
    intent_category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confidence_score: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    primary_intent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    detected_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    message: Mapped["AiMessage"] = relationship("AiMessage", back_populates="intents")
