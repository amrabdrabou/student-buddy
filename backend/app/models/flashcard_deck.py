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
    from app.models.flashcard import Flashcard
    from app.models.ai_conversation import AiConversation


class FlashcardDeck(Base):
    __tablename__ = "flashcard_decks"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    total_cards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mastered_cards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_studied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="flashcard_decks")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="flashcard_decks")
    flashcards: Mapped[List["Flashcard"]] = relationship("Flashcard", back_populates="deck")
    ai_conversations: Mapped[List["AiConversation"]] = relationship("AiConversation", back_populates="related_deck", foreign_keys="AiConversation.related_deck_id")
