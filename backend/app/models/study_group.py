from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.study_group_member import StudyGroupMember
    from app.models.shared_resource import SharedResource


class StudyGroup(Base):
    __tablename__ = "study_groups"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invite_code: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    max_members: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    creator: Mapped["User"] = relationship("User", back_populates="created_study_groups", foreign_keys=[creator_id])
    members: Mapped[List["StudyGroupMember"]] = relationship("StudyGroupMember", back_populates="group")
    shared_resources: Mapped[List["SharedResource"]] = relationship("SharedResource", back_populates="group")
