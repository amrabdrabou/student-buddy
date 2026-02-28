from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_message import AiMessage
    from app.models.study_subject import StudySubject
    from app.models.note import Note


class AiMessageEntity(Base):
    __tablename__ = "ai_message_entities"

    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_messages.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_value: Mapped[str] = mapped_column(Text, nullable=False)
    entity_normalized: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    confidence_score: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    linked_subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    linked_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("notes.id"), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    message: Mapped["AiMessage"] = relationship("AiMessage", back_populates="entities")
    linked_subject: Mapped[Optional["StudySubject"]] = relationship(
        "StudySubject", back_populates="linked_entities", foreign_keys=[linked_subject_id]
    )
    linked_note: Mapped[Optional["Note"]] = relationship(
        "Note", back_populates="linked_entities", foreign_keys=[linked_note_id]
    )
