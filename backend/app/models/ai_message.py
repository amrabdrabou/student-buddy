from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_conversation import AiConversation
    from app.models.ai_message_intent import AiMessageIntent
    from app.models.ai_message_entity import AiMessageEntity
    from app.models.ai_message_feedback import AiMessageFeedback
    from app.models.ai_message_content_store import AiMessageContentStore
    from app.models.ai_message_context import AiMessageContext
    from app.models.embedding_vector import EmbeddingVector


class AiMessage(Base):
    __tablename__ = "ai_messages"
    __table_args__ = (UniqueConstraint("conversation_id", "message_order"),)

    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_conversations.id"), nullable=False)
    parent_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ai_messages.id"), nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_preview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    message_order: Mapped[int] = mapped_column(Integer, nullable=False)
    thread_depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_thread_root: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    context_window_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_large_content: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    conversation: Mapped["AiConversation"] = relationship("AiConversation", back_populates="messages")
    parent_message: Mapped[Optional["AiMessage"]] = relationship(
        "AiMessage", remote_side="AiMessage.id", back_populates="child_messages"
    )
    child_messages: Mapped[List["AiMessage"]] = relationship(
        "AiMessage", back_populates="parent_message"
    )
    intents: Mapped[List["AiMessageIntent"]] = relationship("AiMessageIntent", back_populates="message")
    entities: Mapped[List["AiMessageEntity"]] = relationship("AiMessageEntity", back_populates="message")
    feedback: Mapped[List["AiMessageFeedback"]] = relationship("AiMessageFeedback", back_populates="message")
    content_store: Mapped[Optional["AiMessageContentStore"]] = relationship(
        "AiMessageContentStore", back_populates="message", uselist=False
    )
    contexts: Mapped[List["AiMessageContext"]] = relationship("AiMessageContext", back_populates="message")
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship(
        "EmbeddingVector", back_populates="ai_message", foreign_keys="EmbeddingVector.source_id",
        primaryjoin="and_(EmbeddingVector.source_id == AiMessage.id, EmbeddingVector.source_type == 'ai_message')",
        overlaps="embedding_vectors"
    )
