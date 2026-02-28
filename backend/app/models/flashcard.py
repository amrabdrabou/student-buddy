from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, Text, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base
from app.models.associations import flashcard_tags

if TYPE_CHECKING:
    from app.models.flashcard_deck import FlashcardDeck
    from app.models.flashcard_review import FlashcardReview
    from app.models.tag import Tag
    from app.models.embedding_vector import EmbeddingVector


class Flashcard(Base):
    __tablename__ = "flashcards"

    deck_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("flashcard_decks.id"), nullable=False)
    front_content: Mapped[str] = mapped_column(Text, nullable=False)
    back_content: Mapped[str] = mapped_column(Text, nullable=False)
    front_content_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    back_content_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hint: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ease_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    interval_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    repetitions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    next_review_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_suspended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    deck: Mapped["FlashcardDeck"] = relationship("FlashcardDeck", back_populates="flashcards")
    reviews: Mapped[List["FlashcardReview"]] = relationship("FlashcardReview", back_populates="flashcard")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=flashcard_tags, back_populates="flashcards"
    )
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship(
        "EmbeddingVector", back_populates="flashcard", foreign_keys="EmbeddingVector.source_id",
        primaryjoin="and_(EmbeddingVector.source_id == Flashcard.id, EmbeddingVector.source_type == 'flashcard')",
        overlaps="embedding_vectors"
    )
