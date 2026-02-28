import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SystemPromptBase(BaseModel):
    prompt_name: str
    prompt_category: Optional[str] = None
    description: Optional[str] = None
    system_prompt: str
    user_prompt_template: Optional[str] = None
    recommended_model: Optional[str] = None
    version: int = 1
    is_active: bool = True
    parent_prompt_id: Optional[uuid.UUID] = None


class SystemPromptCreate(SystemPromptBase):
    pass


class SystemPromptUpdate(BaseModel):
    prompt_name: Optional[str] = None
    prompt_category: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    recommended_model: Optional[str] = None
    version: Optional[int] = None
    is_active: Optional[bool] = None
    parent_prompt_id: Optional[uuid.UUID] = None
    times_used: Optional[int] = None
    avg_rating: Optional[Decimal] = None


class SystemPromptResponse(SystemPromptBase):
    id: uuid.UUID
    times_used: int
    avg_rating: Optional[Decimal] = None
    created_at: datetime

    model_config = {"from_attributes": True}
