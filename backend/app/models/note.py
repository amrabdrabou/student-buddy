from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base
from app.models.associations import note_tags

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject
    from app.models.tag import Tag
    from app.models.embedding_vector import EmbeddingVector
    from app.models.ai_gen_note_source import AiGenNoteSource
    from app.models.ai_conversation import AiConversation
    from app.models.ai_message_entity import AiMessageEntity
    from app.models.chatbot_session import ChatbotSession


class Note(Base):
    __tablename__ = "notes"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_format: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    key_concepts: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="notes")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="notes")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=note_tags, back_populates="notes"
    )
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship(
        "EmbeddingVector", back_populates="note", foreign_keys="EmbeddingVector.source_id",
        primaryjoin="and_(EmbeddingVector.source_id == Note.id, EmbeddingVector.source_type == 'note')",
        overlaps="embedding_vectors"
    )
    ai_gen_sources: Mapped[List["AiGenNoteSource"]] = relationship("AiGenNoteSource", back_populates="note")
    ai_conversations: Mapped[List["AiConversation"]] = relationship("AiConversation", back_populates="related_note", foreign_keys="AiConversation.related_note_id")
    linked_entities: Mapped[List["AiMessageEntity"]] = relationship("AiMessageEntity", back_populates="linked_note", foreign_keys="AiMessageEntity.linked_note_id")
    chatbot_sessions_active: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="active_note", foreign_keys="ChatbotSession.active_note_id")
