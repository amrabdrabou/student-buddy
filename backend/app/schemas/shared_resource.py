import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SharedResourceBase(BaseModel):
    group_id: uuid.UUID
    shared_by_user_id: uuid.UUID
    resource_type: str
    resource_id: uuid.UUID
    title: str


class SharedResourceCreate(SharedResourceBase):
    pass


class SharedResourceUpdate(BaseModel):
    resource_type: Optional[str] = None
    resource_id: Optional[uuid.UUID] = None
    title: Optional[str] = None


class SharedResourceResponse(SharedResourceBase):
    id: uuid.UUID
    shared_at: datetime

    model_config = {"from_attributes": True}
