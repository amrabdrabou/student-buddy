from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base

if TYPE_CHECKING:
    from app.models.user_preferences import UserPreferences
    from app.models.study_subject import StudySubject
    from app.models.note import Note
    from app.models.flashcard_deck import FlashcardDeck
    from app.models.document import Document
    from app.models.tag import Tag
    from app.models.study_session import StudySession
    from app.models.study_goal import StudyGoal
    from app.models.daily_progress import DailyProgress
    from app.models.ai_conversation import AiConversation
    from app.models.ai_generated_content import AiGeneratedContent
    from app.models.study_group_member import StudyGroupMember
    from app.models.refresh_token import RefreshToken
    from app.models.ai_usage_stats import AiUsageStats
    from app.models.chatbot_session import ChatbotSession
    from app.models.ai_message_feedback import AiMessageFeedback
    from app.models.embedding_vector import EmbeddingVector
    from app.models.audit_log import AuditLog
    from app.models.study_group import StudyGroup
    from app.models.flashcard_review import FlashcardReview
    from app.models.ai_conversation_metrics import AiConversationMetrics
    from app.models.shared_resource import SharedResource


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    study_goal_minutes_per_day: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    preferences: Mapped[Optional["UserPreferences"]] = relationship("UserPreferences", back_populates="user", uselist=False)
    study_subjects: Mapped[List["StudySubject"]] = relationship("StudySubject", back_populates="user")
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user")
    flashcard_decks: Mapped[List["FlashcardDeck"]] = relationship("FlashcardDeck", back_populates="user")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user")
    tags: Mapped[List["Tag"]] = relationship("Tag", back_populates="user")
    study_sessions: Mapped[List["StudySession"]] = relationship("StudySession", back_populates="user")
    study_goals: Mapped[List["StudyGoal"]] = relationship("StudyGoal", back_populates="user")
    daily_progress: Mapped[List["DailyProgress"]] = relationship("DailyProgress", back_populates="user")
    ai_conversations: Mapped[List["AiConversation"]] = relationship("AiConversation", back_populates="user")
    ai_generated_content: Mapped[List["AiGeneratedContent"]] = relationship("AiGeneratedContent", back_populates="user")
    study_group_members: Mapped[List["StudyGroupMember"]] = relationship("StudyGroupMember", back_populates="user")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    ai_usage_stats: Mapped[List["AiUsageStats"]] = relationship("AiUsageStats", back_populates="user")
    chatbot_sessions: Mapped[List["ChatbotSession"]] = relationship("ChatbotSession", back_populates="user")
    ai_message_feedback: Mapped[List["AiMessageFeedback"]] = relationship("AiMessageFeedback", back_populates="user")
    embedding_vectors: Mapped[List["EmbeddingVector"]] = relationship("EmbeddingVector", back_populates="user")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")
    created_study_groups: Mapped[List["StudyGroup"]] = relationship("StudyGroup", back_populates="creator", foreign_keys="StudyGroup.creator_id")
    flashcard_reviews: Mapped[List["FlashcardReview"]] = relationship("FlashcardReview", back_populates="user")
    ai_conversation_metrics: Mapped[List["AiConversationMetrics"]] = relationship("AiConversationMetrics", back_populates="user")
    shared_resources: Mapped[List["SharedResource"]] = relationship("SharedResource", back_populates="shared_by_user")
