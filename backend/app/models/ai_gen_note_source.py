from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_generated_content import AiGeneratedContent
    from app.models.note import Note


class AiGenNoteSource(Base):
    __tablename__ = "ai_gen_note_sources"

    generated_content_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_generated_content.id"), nullable=False)
    note_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("notes.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    generated_content: Mapped["AiGeneratedContent"] = relationship("AiGeneratedContent", back_populates="note_sources")
    note: Mapped["Note"] = relationship("Note", back_populates="ai_gen_sources")
