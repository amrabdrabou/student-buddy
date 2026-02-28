import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None
    content_format: Optional[str] = None
    summary: Optional[str] = None
    key_concepts: Optional[Dict[str, Any]] = None
    is_pinned: bool = False
    is_archived: bool = False
    subject_id: Optional[uuid.UUID] = None


class NoteCreate(NoteBase):
    user_id: uuid.UUID


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_format: Optional[str] = None
    summary: Optional[str] = None
    key_concepts: Optional[Dict[str, Any]] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    subject_id: Optional[uuid.UUID] = None
    word_count: Optional[int] = None


class NoteResponse(NoteBase):
    id: uuid.UUID
    user_id: uuid.UUID
    word_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
