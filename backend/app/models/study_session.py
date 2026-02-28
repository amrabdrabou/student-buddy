from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject
    from app.models.flashcard_review import FlashcardReview


class StudySession(Base):
    __tablename__ = "study_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    session_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cards_reviewed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cards_correct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    focus_score: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    mood_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="study_sessions")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="study_sessions")
    flashcard_reviews: Mapped[List["FlashcardReview"]] = relationship("FlashcardReview", back_populates="session")
