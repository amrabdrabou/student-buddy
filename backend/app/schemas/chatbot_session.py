import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ChatbotSessionBase(BaseModel):
    user_id: uuid.UUID
    conversation_id: Optional[uuid.UUID] = None
    session_token: str
    device_type: Optional[str] = None
    is_active: bool = True
    session_type: Optional[str] = None
    context_window_size: Optional[int] = None
    active_model: Optional[str] = None
    system_prompt_id: Optional[uuid.UUID] = None
    temperature: Optional[Decimal] = None
    session_params: Optional[Dict[str, Any]] = None
    active_subject_id: Optional[uuid.UUID] = None
    active_note_id: Optional[uuid.UUID] = None
    active_document_id: Optional[uuid.UUID] = None
    expires_at: Optional[datetime] = None


class ChatbotSessionCreate(ChatbotSessionBase):
    pass


class ChatbotSessionUpdate(BaseModel):
    conversation_id: Optional[uuid.UUID] = None
    device_type: Optional[str] = None
    is_active: Optional[bool] = None
    session_type: Optional[str] = None
    context_window_size: Optional[int] = None
    active_model: Optional[str] = None
    system_prompt_id: Optional[uuid.UUID] = None
    temperature: Optional[Decimal] = None
    session_params: Optional[Dict[str, Any]] = None
    active_subject_id: Optional[uuid.UUID] = None
    active_note_id: Optional[uuid.UUID] = None
    active_document_id: Optional[uuid.UUID] = None
    last_activity_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    messages_in_session: Optional[int] = None
    tokens_used_in_session: Optional[int] = None


class ChatbotSessionResponse(ChatbotSessionBase):
    id: uuid.UUID
    started_at: datetime
    last_activity_at: Optional[datetime] = None
    messages_in_session: int
    tokens_used_in_session: int

    model_config = {"from_attributes": True}
