import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AiMessageContentStoreBase(BaseModel):
    message_id: uuid.UUID
    content_type: str
    content_size_bytes: Optional[int] = None
    content_text: Optional[str] = None
    storage_provider: Optional[str] = None
    storage_key: Optional[str] = None
    is_external: bool = False


class AiMessageContentStoreCreate(AiMessageContentStoreBase):
    pass


class AiMessageContentStoreUpdate(BaseModel):
    content_type: Optional[str] = None
    content_size_bytes: Optional[int] = None
    content_text: Optional[str] = None
    storage_provider: Optional[str] = None
    storage_key: Optional[str] = None
    is_external: Optional[bool] = None


class AiMessageContentStoreResponse(AiMessageContentStoreBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
