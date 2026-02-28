import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class FlashcardReviewBase(BaseModel):
    flashcard_id: uuid.UUID
    user_id: uuid.UUID
    session_id: Optional[uuid.UUID] = None
    quality_rating: Optional[int] = None
    response_time_seconds: Optional[int] = None
    previous_ease_factor: Optional[Decimal] = None
    new_ease_factor: Optional[Decimal] = None
    previous_interval: Optional[int] = None
    new_interval: Optional[int] = None


class FlashcardReviewCreate(FlashcardReviewBase):
    pass


class FlashcardReviewUpdate(BaseModel):
    quality_rating: Optional[int] = None
    response_time_seconds: Optional[int] = None
    previous_ease_factor: Optional[Decimal] = None
    new_ease_factor: Optional[Decimal] = None
    previous_interval: Optional[int] = None
    new_interval: Optional[int] = None


class FlashcardReviewResponse(FlashcardReviewBase):
    id: uuid.UUID
    reviewed_at: datetime

    model_config = {"from_attributes": True}
