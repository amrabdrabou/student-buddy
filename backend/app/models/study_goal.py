from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_subject import StudySubject


class StudyGoal(Base):
    __tablename__ = "study_goals"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("study_subjects.id"), nullable=True)
    goal_type: Mapped[str] = mapped_column(String, nullable=False)
    target_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    current_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="study_goals")
    subject: Mapped[Optional["StudySubject"]] = relationship("StudySubject", back_populates="study_goals")
