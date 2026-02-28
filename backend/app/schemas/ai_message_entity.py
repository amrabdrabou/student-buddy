import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AiMessageEntityBase(BaseModel):
    message_id: uuid.UUID
    entity_type: str
    entity_value: str
    entity_normalized: Optional[str] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    confidence_score: Optional[Decimal] = None
    linked_subject_id: Optional[uuid.UUID] = None
    linked_note_id: Optional[uuid.UUID] = None


class AiMessageEntityCreate(AiMessageEntityBase):
    pass


class AiMessageEntityUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_value: Optional[str] = None
    entity_normalized: Optional[str] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    confidence_score: Optional[Decimal] = None
    linked_subject_id: Optional[uuid.UUID] = None
    linked_note_id: Optional[uuid.UUID] = None


class AiMessageEntityResponse(AiMessageEntityBase):
    id: uuid.UUID
    detected_at: datetime

    model_config = {"from_attributes": True}
