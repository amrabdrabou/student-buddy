import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class StudySessionBase(BaseModel):
    user_id: uuid.UUID
    subject_id: Optional[uuid.UUID] = None
    session_type: Optional[str] = None


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionUpdate(BaseModel):
    subject_id: Optional[uuid.UUID] = None
    session_type: Optional[str] = None
    ended_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    cards_reviewed: Optional[int] = None
    cards_correct: Optional[int] = None
    focus_score: Optional[Decimal] = None
    mood_rating: Optional[int] = None
    is_completed: Optional[bool] = None


class StudySessionResponse(StudySessionBase):
    id: uuid.UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    cards_reviewed: int
    cards_correct: int
    focus_score: Optional[Decimal] = None
    mood_rating: Optional[int] = None
    is_completed: bool

    model_config = {"from_attributes": True}
