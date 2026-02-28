import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AiUsageStatsBase(BaseModel):
    user_id: uuid.UUID
    stat_date: date
    stat_period: Optional[str] = None
    conversations_started: int = 0
    conversations_completed: int = 0
    total_messages_sent: int = 0
    total_tokens_consumed: int = 0
    estimated_cost_usd: Optional[Decimal] = None
    flashcards_generated: int = 0
    summaries_generated: int = 0
    avg_conversation_duration_minutes: Optional[int] = None


class AiUsageStatsCreate(AiUsageStatsBase):
    pass


class AiUsageStatsUpdate(BaseModel):
    stat_period: Optional[str] = None
    conversations_started: Optional[int] = None
    conversations_completed: Optional[int] = None
    total_messages_sent: Optional[int] = None
    total_tokens_consumed: Optional[int] = None
    estimated_cost_usd: Optional[Decimal] = None
    flashcards_generated: Optional[int] = None
    summaries_generated: Optional[int] = None
    avg_conversation_duration_minutes: Optional[int] = None


class AiUsageStatsResponse(AiUsageStatsBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
