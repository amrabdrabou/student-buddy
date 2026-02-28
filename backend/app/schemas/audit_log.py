import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AuditLogBase(BaseModel):
    user_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[uuid.UUID] = None
    action_description: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    action_result: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogUpdate(BaseModel):
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[uuid.UUID] = None
    action_description: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    action_result: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
