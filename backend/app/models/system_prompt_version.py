from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.system_prompt import SystemPrompt


class SystemPromptVersion(Base):
    __tablename__ = "system_prompt_versions"
    __table_args__ = (UniqueConstraint("prompt_id", "version_number"),)

    prompt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("system_prompts.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    change_description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    prompt: Mapped["SystemPrompt"] = relationship("SystemPrompt", back_populates="versions")
