import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class DocumentBase(BaseModel):
    title: str
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    subject_id: Optional[uuid.UUID] = None


class DocumentCreate(DocumentBase):
    user_id: uuid.UUID
    processing_status: str = "pending"


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    subject_id: Optional[uuid.UUID] = None
    processing_status: Optional[str] = None
    extracted_text: Optional[str] = None
    page_count: Optional[int] = None
    summary: Optional[str] = None
    topics: Optional[Dict[str, Any]] = None
    processed_at: Optional[datetime] = None


class DocumentResponse(DocumentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    processing_status: str
    extracted_text: Optional[str] = None
    page_count: Optional[int] = None
    summary: Optional[str] = None
    topics: Optional[Dict[str, Any]] = None
    uploaded_at: datetime
    processed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
