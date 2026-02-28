from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.note import Note
    from app.models.flashcard_deck import FlashcardDeck
    from app.models.document import Document
    from app.models.study_session import StudySession
    from app.models.study_goal import StudyGoal
    from app.models.ai_conversation import AiConversation
    from app.models.embedding_vector import EmbeddingVector
    from app.models.ai_message_entity import AiMessageEntity
    from app.models.chatbot_session import ChatbotSession
    from app.models.ai_conversation_metrics import AiConversationMetrics


class StudySubject(Base):
    __tablename__ = "study_subjects"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    color_hex: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="study_subjects")
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="subject")
    flashcard_decks: Mapped[List["FlashcardDeck"]] = relationship("FlashcardDeck", back_populates="subject")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="subject")
    study_sessions: Mapped[List["StudySession"]] = relationship("StudySession", back_populates="subject")
    study_goals: Mapped[List["StudyGoal"]] = relationship("StudyGoal", back_populates="subject")
    ai_conversations: Mapped[List["AiConversation"]] = relationship("AiConversation", back_populates="subject")
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship("EmbeddingVector", back_populates="subject", foreign_keys="EmbeddingVector.subject_id")
    linked_entities: Mapped[List["AiMessageEntity"]] = relationship("AiMessageEntity", back_populates="linked_subject", foreign_keys="AiMessageEntity.linked_subject_id")
    chatbot_sessions_active: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="active_subject", foreign_keys="ChatbotSession.active_subject_id")
    conversation_metrics: Mapped[List["AiConversationMetrics"]] = relationship("AiConversationMetrics", back_populates="primary_subject", foreign_keys="AiConversationMetrics.primary_subject_id")
