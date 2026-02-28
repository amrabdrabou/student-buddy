import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudyGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False
    invite_code: Optional[str] = None
    max_members: Optional[int] = None


class StudyGroupCreate(StudyGroupBase):
    creator_id: uuid.UUID


class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None
    invite_code: Optional[str] = None
    max_members: Optional[int] = None


class StudyGroupResponse(StudyGroupBase):
    id: uuid.UUID
    creator_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
