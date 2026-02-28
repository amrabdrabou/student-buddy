import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AiMessageIntentBase(BaseModel):
    message_id: uuid.UUID
    intent_type: str
    intent_category: Optional[str] = None
    confidence_score: Optional[Decimal] = None
    primary_intent: bool = False
    detected_by: Optional[str] = None


class AiMessageIntentCreate(AiMessageIntentBase):
    pass


class AiMessageIntentUpdate(BaseModel):
    intent_type: Optional[str] = None
    intent_category: Optional[str] = None
    confidence_score: Optional[Decimal] = None
    primary_intent: Optional[bool] = None
    detected_by: Optional[str] = None


class AiMessageIntentResponse(AiMessageIntentBase):
    id: uuid.UUID
    detected_at: datetime

    model_config = {"from_attributes": True}
