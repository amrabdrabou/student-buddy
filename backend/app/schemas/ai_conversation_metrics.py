import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AiConversationMetricsBase(BaseModel):
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    total_messages: int = 0
    user_messages: int = 0
    assistant_messages: int = 0
    total_tokens_used: int = 0
    avg_tokens_per_message: Optional[Decimal] = None
    avg_response_time_ms: Optional[int] = None
    thread_depth_max: int = 0
    conversation_completed: bool = False
    user_rating: Optional[int] = None
    primary_subject_id: Optional[uuid.UUID] = None
    detected_topics: Optional[Dict[str, Any]] = None


class AiConversationMetricsCreate(AiConversationMetricsBase):
    pass


class AiConversationMetricsUpdate(BaseModel):
    total_messages: Optional[int] = None
    user_messages: Optional[int] = None
    assistant_messages: Optional[int] = None
    total_tokens_used: Optional[int] = None
    avg_tokens_per_message: Optional[Decimal] = None
    avg_response_time_ms: Optional[int] = None
    thread_depth_max: Optional[int] = None
    conversation_completed: Optional[bool] = None
    user_rating: Optional[int] = None
    primary_subject_id: Optional[uuid.UUID] = None
    detected_topics: Optional[Dict[str, Any]] = None


class AiConversationMetricsResponse(AiConversationMetricsBase):
    id: uuid.UUID
    calculated_at: datetime

    model_config = {"from_attributes": True}
