import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudyGroupMemberBase(BaseModel):
    group_id: uuid.UUID
    user_id: uuid.UUID
    role: str


class StudyGroupMemberCreate(StudyGroupMemberBase):
    pass


class StudyGroupMemberUpdate(BaseModel):
    role: Optional[str] = None


class StudyGroupMemberResponse(StudyGroupMemberBase):
    id: uuid.UUID
    joined_at: datetime

    model_config = {"from_attributes": True}
