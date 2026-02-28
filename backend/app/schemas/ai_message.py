import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AiMessageBase(BaseModel):
    conversation_id: uuid.UUID
    parent_message_id: Optional[uuid.UUID] = None
    role: str
    content: Optional[str] = None
    content_preview: Optional[str] = None
    message_order: int
    thread_depth: int = 0
    is_thread_root: bool = True
    context_window_position: Optional[int] = None
    has_large_content: bool = False
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    processing_time_ms: Optional[int] = None


class AiMessageCreate(AiMessageBase):
    pass


class AiMessageUpdate(BaseModel):
    content: Optional[str] = None
    content_preview: Optional[str] = None
    context_window_position: Optional[int] = None
    has_large_content: Optional[bool] = None
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    processing_time_ms: Optional[int] = None


class AiMessageResponse(AiMessageBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
