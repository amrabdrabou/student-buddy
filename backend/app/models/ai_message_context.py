from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.ai_message import AiMessage
    from app.models.ai_conversation import AiConversation


class AiMessageContext(Base):
    __tablename__ = "ai_message_contexts"

    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_messages.id"), nullable=False)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_conversations.id"), nullable=False)
    context_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    retrieved_chunks: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    retrieval_query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retrieval_method: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    context_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    key_entities: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    context_embedding: Mapped[Optional[List[float]]] = mapped_column(Vector, nullable=True)
    source_notes: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(ForeignKey("notes.id")), nullable=True)
    source_documents: Mapped[Optional[List[uuid.UUID]]] = mapped_column(ARRAY(ForeignKey("documents.id")), nullable=True)
    tokens_in_context: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    relevance_score: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    message: Mapped["AiMessage"] = relationship("AiMessage", back_populates="contexts")
    conversation: Mapped["AiConversation"] = relationship("AiConversation", back_populates="message_contexts")
