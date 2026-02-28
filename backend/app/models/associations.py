from __future__ import annotations

import uuid

from sqlalchemy import Column, ForeignKey, Table

from app.core.db_setup import Base

flashcard_tags = Table(
    "flashcard_tags",
    Base.metadata,
    Column("flashcard_id", ForeignKey("flashcards.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("document_id", ForeignKey("documents.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
