import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AiGenDocumentSourceBase(BaseModel):
    generated_content_id: uuid.UUID
    document_id: uuid.UUID


class AiGenDocumentSourceCreate(AiGenDocumentSourceBase):
    pass


class AiGenDocumentSourceUpdate(BaseModel):
    generated_content_id: Optional[uuid.UUID] = None
    document_id: Optional[uuid.UUID] = None


class AiGenDocumentSourceResponse(AiGenDocumentSourceBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
