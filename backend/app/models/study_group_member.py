from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.study_group import StudyGroup
    from app.models.user import User


class StudyGroupMember(Base):
    __tablename__ = "study_group_members"

    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("study_groups.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    group: Mapped["StudyGroup"] = relationship("StudyGroup", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="study_group_members")
