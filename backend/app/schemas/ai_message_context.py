import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AiMessageContextBase(BaseModel):
    message_id: uuid.UUID
    conversation_id: uuid.UUID
    context_type: Optional[str] = None
    retrieved_chunks: Optional[Dict[str, Any]] = None
    retrieval_query: Optional[str] = None
    retrieval_method: Optional[str] = None
    context_summary: Optional[str] = None
    key_entities: Optional[Dict[str, Any]] = None
    context_embedding: Optional[List[float]] = None
    source_notes: Optional[List[uuid.UUID]] = None
    source_documents: Optional[List[uuid.UUID]] = None
    tokens_in_context: Optional[int] = None
    relevance_score: Optional[Decimal] = None


class AiMessageContextCreate(AiMessageContextBase):
    pass


class AiMessageContextUpdate(BaseModel):
    context_type: Optional[str] = None
    retrieved_chunks: Optional[Dict[str, Any]] = None
    retrieval_query: Optional[str] = None
    retrieval_method: Optional[str] = None
    context_summary: Optional[str] = None
    key_entities: Optional[Dict[str, Any]] = None
    context_embedding: Optional[List[float]] = None
    source_notes: Optional[List[uuid.UUID]] = None
    source_documents: Optional[List[uuid.UUID]] = None
    tokens_in_context: Optional[int] = None
    relevance_score: Optional[Decimal] = None


class AiMessageContextResponse(AiMessageContextBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
