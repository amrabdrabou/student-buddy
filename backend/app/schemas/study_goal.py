import uuid
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class StudyGoalBase(BaseModel):
    user_id: uuid.UUID
    subject_id: Optional[uuid.UUID] = None
    goal_type: str
    target_value: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True


class StudyGoalCreate(StudyGoalBase):
    pass


class StudyGoalUpdate(BaseModel):
    subject_id: Optional[uuid.UUID] = None
    goal_type: Optional[str] = None
    target_value: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    is_completed: Optional[bool] = None


class StudyGoalResponse(StudyGoalBase):
    id: uuid.UUID
    current_value: Optional[Decimal] = None
    is_completed: bool

    model_config = {"from_attributes": True}
