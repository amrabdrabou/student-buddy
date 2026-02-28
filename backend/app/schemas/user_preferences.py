import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class UserPreferencesBase(BaseModel):
    preferred_ai_model: Optional[str] = None
    preferred_temperature: Optional[Decimal] = None
    preferred_max_tokens: Optional[int] = None
    conversation_style: Optional[str] = None
    explanation_depth: Optional[str] = None
    preferred_language: Optional[str] = None
    enable_socratic_mode: bool = False
    enable_step_by_step: bool = False
    enable_rag_context: bool = False
    max_context_messages: Optional[int] = None


class UserPreferencesCreate(UserPreferencesBase):
    user_id: uuid.UUID


class UserPreferencesUpdate(BaseModel):
    preferred_ai_model: Optional[str] = None
    preferred_temperature: Optional[Decimal] = None
    preferred_max_tokens: Optional[int] = None
    conversation_style: Optional[str] = None
    explanation_depth: Optional[str] = None
    preferred_language: Optional[str] = None
    enable_socratic_mode: Optional[bool] = None
    enable_step_by_step: Optional[bool] = None
    enable_rag_context: Optional[bool] = None
    max_context_messages: Optional[int] = None


class UserPreferencesResponse(UserPreferencesBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
