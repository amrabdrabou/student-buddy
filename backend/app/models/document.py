from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base
from app.models.associations import document_tags

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject
    from app.models.tag import Tag
    from app.models.embedding_vector import EmbeddingVector
    from app.models.ai_gen_document_source import AiGenDocumentSource
    from app.models.ai_conversation import AiConversation
    from app.models.chatbot_session import ChatbotSession


class Document(Base):
    __tablename__ = "documents"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    processing_status: Mapped[str] = mapped_column(String, nullable=False)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    topics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="documents")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="documents")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=document_tags, back_populates="documents"
    )
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship(
        "EmbeddingVector", back_populates="parent_document", foreign_keys="EmbeddingVector.parent_document_id"
    )
    ai_gen_sources: Mapped[List["AiGenDocumentSource"]] = relationship("AiGenDocumentSource", back_populates="document")
    ai_conversations: Mapped[List["AiConversation"]] = relationship("AiConversation", back_populates="related_document", foreign_keys="AiConversation.related_document_id")
    chatbot_sessions_active: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="active_document", foreign_keys="ChatbotSession.active_document_id")
