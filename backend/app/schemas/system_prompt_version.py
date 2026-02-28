import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SystemPromptVersionBase(BaseModel):
    prompt_id: uuid.UUID
    version_number: int
    system_prompt: str
    user_prompt_template: str
    change_description: str


class SystemPromptVersionCreate(SystemPromptVersionBase):
    pass


class SystemPromptVersionUpdate(BaseModel):
    version_number: Optional[int] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    change_description: Optional[str] = None


class SystemPromptVersionResponse(SystemPromptVersionBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
