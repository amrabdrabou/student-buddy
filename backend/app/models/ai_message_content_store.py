from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, LargeBinary, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_message import AiMessage


class AiMessageContentStore(Base):
    __tablename__ = "ai_message_content_store"
    __table_args__ = (UniqueConstraint("message_id"),)

    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_messages.id"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    content_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_binary: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    storage_provider: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    storage_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    message: Mapped["AiMessage"] = relationship("AiMessage", back_populates="content_store")
