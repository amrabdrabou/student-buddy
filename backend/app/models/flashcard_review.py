from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.flashcard import Flashcard
    from app.models.study_session import StudySession
    from app.models.user import User


class FlashcardReview(Base):
    __tablename__ = "flashcard_reviews"

    flashcard_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("flashcards.id"), nullable=False)
    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_sessions.id"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    quality_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    previous_ease_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    new_ease_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    previous_interval: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    new_interval: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    flashcard: Mapped["Flashcard"] = relationship("Flashcard", back_populates="reviews")
    session: Mapped[Optional["StudySession"]] = relationship("StudySession", back_populates="flashcard_reviews")
    user: Mapped["User"] = relationship("User", back_populates="flashcard_reviews")
