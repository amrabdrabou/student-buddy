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


class SharedResource(Base):
    __tablename__ = "shared_resources"

    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("study_groups.id"), nullable=False)
    shared_by_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    resource_type: Mapped[str] = mapped_column(String, nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    shared_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    group: Mapped["StudyGroup"] = relationship("StudyGroup", back_populates="shared_resources")
    shared_by_user: Mapped["User"] = relationship("User", back_populates="shared_resources")
