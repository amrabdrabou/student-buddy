import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class EmbeddingVectorBase(BaseModel):
    source_type: str
    source_id: uuid.UUID
    user_id: uuid.UUID
    content_text: Optional[str] = None
    content_hash: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    subject_id: Optional[uuid.UUID] = None
    content_type: Optional[str] = None
    chunk_index: Optional[int] = None
    parent_document_id: Optional[uuid.UUID] = None
    token_count: Optional[int] = None


class EmbeddingVectorCreate(EmbeddingVectorBase):
    pass


class EmbeddingVectorUpdate(BaseModel):
    content_text: Optional[str] = None
    content_hash: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    subject_id: Optional[uuid.UUID] = None
    content_type: Optional[str] = None
    chunk_index: Optional[int] = None
    parent_document_id: Optional[uuid.UUID] = None
    token_count: Optional[int] = None


class EmbeddingVectorResponse(EmbeddingVectorBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
