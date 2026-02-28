from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject
    from app.models.document import Document
    from app.models.note import Note
    from app.models.flashcard import Flashcard
    from app.models.ai_message import AiMessage


class EmbeddingVector(Base):
    __tablename__ = "embedding_vectors"

    source_type: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector, nullable=True)
    embedding_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    chunk_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    parent_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("documents.id"), nullable=True)
    token_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="embedding_vectors")
    subject: Mapped[Optional["StudySubject"]] = relationship(
        "StudySubject", back_populates="embedding_vectors", foreign_keys=[subject_id]
    )
    parent_document: Mapped[Optional["Document"]] = relationship(
        "Document", back_populates="embedding_vectors", foreign_keys=[parent_document_id]
    )
    note: Mapped[Optional["Note"]] = relationship(
        "Note",
        back_populates="embedding_vectors",
        foreign_keys=[source_id],
        primaryjoin="and_(EmbeddingVector.source_id == Note.id, EmbeddingVector.source_type == 'note')",
        overlaps="embedding_vectors,flashcard,ai_message"
    )
    flashcard: Mapped[Optional["Flashcard"]] = relationship(
        "Flashcard",
        back_populates="embedding_vectors",
        foreign_keys=[source_id],
        primaryjoin="and_(EmbeddingVector.source_id == Flashcard.id, EmbeddingVector.source_type == 'flashcard')",
        overlaps="embedding_vectors,note,ai_message"
    )
    ai_message: Mapped[Optional["AiMessage"]] = relationship(
        "AiMessage",
        back_populates="embedding_vectors",
        foreign_keys=[source_id],
        primaryjoin="and_(EmbeddingVector.source_id == AiMessage.id, EmbeddingVector.source_type == 'ai_message')",
        overlaps="embedding_vectors,note,flashcard"
    )
