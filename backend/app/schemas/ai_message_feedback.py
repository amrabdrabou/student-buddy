import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AiMessageFeedbackBase(BaseModel):
    message_id: uuid.UUID
    user_id: uuid.UUID
    conversation_id: uuid.UUID
    feedback_type: Optional[str] = None
    rating: Optional[int] = None
    is_helpful: Optional[bool] = None
    is_accurate: Optional[bool] = None
    feedback_categories: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None
    reported_issue: Optional[str] = None


class AiMessageFeedbackCreate(AiMessageFeedbackBase):
    pass


class AiMessageFeedbackUpdate(BaseModel):
    feedback_type: Optional[str] = None
    rating: Optional[int] = None
    is_helpful: Optional[bool] = None
    is_accurate: Optional[bool] = None
    feedback_categories: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None
    reported_issue: Optional[str] = None


class AiMessageFeedbackResponse(AiMessageFeedbackBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
