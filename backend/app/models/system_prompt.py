from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.system_prompt_version import SystemPromptVersion
    from app.models.chatbot_session import ChatbotSession


class SystemPrompt(Base):
    __tablename__ = "system_prompts"

    prompt_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    prompt_category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_prompt_template: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    parent_prompt_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("system_prompts.id"), nullable=True)
    times_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_rating: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    parent_prompt: Mapped[Optional["SystemPrompt"]] = relationship(
        "SystemPrompt", remote_side="SystemPrompt.id", back_populates="child_prompts"
    )
    child_prompts: Mapped[List["SystemPrompt"]] = relationship(
        "SystemPrompt", back_populates="parent_prompt"
    )
    versions: Mapped[List["SystemPromptVersion"]] = relationship("SystemPromptVersion", back_populates="prompt")
    chatbot_sessions: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="system_prompt")
