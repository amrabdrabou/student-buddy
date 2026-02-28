import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RefreshTokenBase(BaseModel):
    user_id: uuid.UUID
    token: str
    expires_at: datetime
    revoked: bool = False


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenUpdate(BaseModel):
    revoked: Optional[bool] = None
    expires_at: Optional[datetime] = None


class RefreshTokenResponse(RefreshTokenBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
