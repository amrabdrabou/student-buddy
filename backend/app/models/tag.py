from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_setup import Base
from app.models.associations import flashcard_tags, note_tags, document_tags

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.flashcard import Flashcard
    from app.models.note import Note
    from app.models.document import Document


class Tag(Base):
    __tablename__ = "tags"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="tags")
    flashcards: Mapped[List["Flashcard"]] = relationship(
        "Flashcard", secondary=flashcard_tags, back_populates="tags"
    )
    notes: Mapped[List["Note"]] = relationship(
        "Note", secondary=note_tags, back_populates="tags"
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document", secondary=document_tags, back_populates="tags"
    )
