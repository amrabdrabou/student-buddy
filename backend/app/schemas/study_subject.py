import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudySubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color_hex: Optional[str] = None
    is_archived: bool = False


class StudySubjectCreate(StudySubjectBase):
    user_id: uuid.UUID


class StudySubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color_hex: Optional[str] = None
    is_archived: Optional[bool] = None


class StudySubjectResponse(StudySubjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
