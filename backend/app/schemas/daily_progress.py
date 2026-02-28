import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class DailyProgressBase(BaseModel):
    user_id: uuid.UUID
    date: date
    total_study_minutes: int = 0
    cards_reviewed: int = 0
    cards_mastered: int = 0
    notes_created: int = 0
    streak_days: int = 0


class DailyProgressCreate(DailyProgressBase):
    pass


class DailyProgressUpdate(BaseModel):
    total_study_minutes: Optional[int] = None
    cards_reviewed: Optional[int] = None
    cards_mastered: Optional[int] = None
    notes_created: Optional[int] = None
    streak_days: Optional[int] = None


class DailyProgressResponse(DailyProgressBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
