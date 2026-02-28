from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.ai_conversation import AiConversation
    from app.models.system_prompt import SystemPrompt
    from app.models.study_subject import StudySubject
    from app.models.note import Note
    from app.models.document import Document


class ChatbotSession(Base):
    __tablename__ = "chatbot_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ai_conversations.id"), nullable=True)
    session_token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    device_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    session_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    context_window_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    system_prompt_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("system_prompts.id"), nullable=True)
    temperature: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    session_params: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    active_subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    active_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("notes.id"), nullable=True)
    active_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("documents.id"), nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    messages_in_session: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tokens_used_in_session: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="chatbot_sessions")
    conversation: Mapped[Optional["AiConversation"]] = relationship("AiConversation", back_populates="chatbot_sessions")
    system_prompt: Mapped[Optional["SystemPrompt"]] = relationship("SystemPrompt", back_populates="chatbot_sessions")
    active_subject: Mapped[Optional["StudySubject"]] = relationship(
        "StudySubject", back_populates="chatbot_sessions_active", foreign_keys=[active_subject_id]
    )
    active_note: Mapped[Optional["Note"]] = relationship(
        "Note", back_populates="chatbot_sessions_active", foreign_keys=[active_note_id]
    )
    active_document: Mapped[Optional["Document"]] = relationship(
        "Document", back_populates="chatbot_sessions_active", foreign_keys=[active_document_id]
    )
