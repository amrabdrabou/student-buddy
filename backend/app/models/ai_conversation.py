from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject
    from app.models.note import Note
    from app.models.document import Document
    from app.models.flashcard_deck import FlashcardDeck
    from app.models.ai_message import AiMessage
    from app.models.ai_conversation_metrics import AiConversationMetrics
    from app.models.ai_message_feedback import AiMessageFeedback
    from app.models.chatbot_session import ChatbotSession
    from app.models.ai_message_context import AiMessageContext


class AiConversation(Base):
    __tablename__ = "ai_conversations"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    conversation_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    related_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("notes.id"), nullable=True)
    related_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("documents.id"), nullable=True)
    related_deck_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("flashcard_decks.id"), nullable=True)
    total_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="ai_conversations")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="ai_conversations")
    related_note: Mapped[Optional["Note"]] = relationship("Note", back_populates="ai_conversations", foreign_keys=[related_note_id])
    related_document: Mapped[Optional["Document"]] = relationship("Document", back_populates="ai_conversations", foreign_keys=[related_document_id])
    related_deck: Mapped[Optional["FlashcardDeck"]] = relationship("FlashcardDeck", back_populates="ai_conversations", foreign_keys=[related_deck_id])
    messages: Mapped[List["AiMessage"]] = relationship("AiMessage", back_populates="conversation")
    metrics: Mapped[Optional["AiConversationMetrics"]] = relationship("AiConversationMetrics", back_populates="conversation", uselist=False)
    feedback: Mapped[List["AiMessageFeedback"]] = relationship("AiMessageFeedback", back_populates="conversation")
    chatbot_sessions: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="conversation")
    message_contexts: Mapped[List["AiMessageContext"]] = relationship("AiMessageContext", back_populates="conversation")
