import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FlashcardDeckBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject_id: Optional[uuid.UUID] = None
    is_public: bool = False
    is_archived: bool = False


class FlashcardDeckCreate(FlashcardDeckBase):
    user_id: uuid.UUID


class FlashcardDeckUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject_id: Optional[uuid.UUID] = None
    is_public: Optional[bool] = None
    is_archived: Optional[bool] = None
    total_cards: Optional[int] = None
    mastered_cards: Optional[int] = None
    last_studied_at: Optional[datetime] = None


class FlashcardDeckResponse(FlashcardDeckBase):
    id: uuid.UUID
    user_id: uuid.UUID
    total_cards: int
    mastered_cards: int
    created_at: datetime
    last_studied_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
