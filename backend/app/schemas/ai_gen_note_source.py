import uuid
from datetime import datetime

from pydantic import BaseModel


class AiGenNoteSourceBase(BaseModel):
    generated_content_id: uuid.UUID
    note_id: uuid.UUID


class AiGenNoteSourceCreate(AiGenNoteSourceBase):
    pass


class AiGenNoteSourceUpdate(BaseModel):
    generated_content_id: uuid.UUID | None = None
    note_id: uuid.UUID | None = None


class AiGenNoteSourceResponse(AiGenNoteSourceBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
