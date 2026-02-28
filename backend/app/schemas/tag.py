import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    user_id: uuid.UUID


class TagUpdate(BaseModel):
    name: Optional[str] = None


class TagResponse(TagBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
