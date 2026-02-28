import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AiConversationBase(BaseModel):
    user_id: uuid.UUID
    subject_id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    conversation_type: Optional[str] = None
    related_note_id: Optional[uuid.UUID] = None
    related_document_id: Optional[uuid.UUID] = None
    related_deck_id: Optional[uuid.UUID] = None
    is_archived: bool = False


class AiConversationCreate(AiConversationBase):
    pass


class AiConversationUpdate(BaseModel):
    subject_id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    conversation_type: Optional[str] = None
    related_note_id: Optional[uuid.UUID] = None
    related_document_id: Optional[uuid.UUID] = None
    related_deck_id: Optional[uuid.UUID] = None
    is_archived: Optional[bool] = None
    total_messages: Optional[int] = None
    last_message_at: Optional[datetime] = None


class AiConversationResponse(AiConversationBase):
    id: uuid.UUID
    total_messages: int
    created_at: datetime
    last_message_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
