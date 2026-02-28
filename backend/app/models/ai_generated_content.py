from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.ai_gen_note_source import AiGenNoteSource
    from app.models.ai_gen_document_source import AiGenDocumentSource


class AiGeneratedContent(Base):
    __tablename__ = "ai_generated_content"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    source_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True)
    input_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generated_content: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    user_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    was_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    was_saved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    model_used: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="ai_generated_content")
    note_sources: Mapped[List["AiGenNoteSource"]] = relationship("AiGenNoteSource", back_populates="generated_content")
    document_sources: Mapped[List["AiGenDocumentSource"]] = relationship("AiGenDocumentSource", back_populates="generated_content")
