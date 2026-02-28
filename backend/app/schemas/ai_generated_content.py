import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AiGeneratedContentBase(BaseModel):
    user_id: uuid.UUID
    content_type: str
    source_type: Optional[str] = None
    source_id: Optional[uuid.UUID] = None
    input_text: Optional[str] = None
    generated_content: Optional[Dict[str, Any]] = None
    user_rating: Optional[int] = None
    was_edited: bool = False
    was_saved: bool = False
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None


class AiGeneratedContentCreate(AiGeneratedContentBase):
    pass


class AiGeneratedContentUpdate(BaseModel):
    content_type: Optional[str] = None
    source_type: Optional[str] = None
    source_id: Optional[uuid.UUID] = None
    input_text: Optional[str] = None
    generated_content: Optional[Dict[str, Any]] = None
    user_rating: Optional[int] = None
    was_edited: Optional[bool] = None
    was_saved: Optional[bool] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None


class AiGeneratedContentResponse(AiGeneratedContentBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
