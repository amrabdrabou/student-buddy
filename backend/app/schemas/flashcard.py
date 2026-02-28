import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class FlashcardBase(BaseModel):
    front_content: str
    back_content: str
    front_content_type: Optional[str] = None
    back_content_type: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None
    difficulty_rating: Optional[int] = None


class FlashcardCreate(FlashcardBase):
    deck_id: uuid.UUID


class FlashcardUpdate(BaseModel):
    front_content: Optional[str] = None
    back_content: Optional[str] = None
    front_content_type: Optional[str] = None
    back_content_type: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None
    difficulty_rating: Optional[int] = None
    ease_factor: Optional[Decimal] = None
    interval_days: Optional[int] = None
    repetitions: Optional[int] = None
    next_review_date: Optional[datetime] = None
    total_reviews: Optional[int] = None
    correct_reviews: Optional[int] = None
    is_suspended: Optional[bool] = None


class FlashcardResponse(FlashcardBase):
    id: uuid.UUID
    deck_id: uuid.UUID
    ease_factor: Optional[Decimal] = None
    interval_days: int
    repetitions: int
    next_review_date: Optional[datetime] = None
    total_reviews: int
    correct_reviews: int
    is_suspended: bool
    created_at: datetime

    model_config = {"from_attributes": True}
