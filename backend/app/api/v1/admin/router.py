import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.audit_log import AuditLog
from app.models.system_prompt import SystemPrompt
from app.models.system_prompt_version import SystemPromptVersion
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse
from app.schemas.system_prompt import SystemPromptCreate, SystemPromptUpdate, SystemPromptResponse
from app.schemas.system_prompt_version import SystemPromptVersionResponse
from app.schemas.user import UserResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/system-prompts", response_model=List[SystemPromptResponse])
async def list_system_prompts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[SystemPromptResponse]:
    result = await db.execute(
        select(SystemPrompt).order_by(SystemPrompt.created_at.desc())
    )
    prompts = result.scalars().all()
    return [SystemPromptResponse.model_validate(p) for p in prompts]


@router.post("/system-prompts", response_model=SystemPromptResponse, status_code=status.HTTP_201_CREATED)
async def create_system_prompt(
    payload: SystemPromptCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SystemPromptResponse:
    existing = await db.execute(
        select(SystemPrompt).where(SystemPrompt.prompt_name == payload.prompt_name)
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A system prompt with this name already exists",
        )

    prompt = SystemPrompt(
        prompt_name=payload.prompt_name,
        prompt_category=payload.prompt_category,
        description=payload.description,
        system_prompt=payload.system_prompt,
        user_prompt_template=payload.user_prompt_template,
        recommended_model=payload.recommended_model,
        version=payload.version,
        is_active=payload.is_active,
        parent_prompt_id=payload.parent_prompt_id,
    )
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    return SystemPromptResponse.model_validate(prompt)


@router.get("/system-prompts/{prompt_id}", response_model=SystemPromptResponse)
async def get_system_prompt(
    prompt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SystemPromptResponse:
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System prompt not found")
    return SystemPromptResponse.model_validate(prompt)


@router.patch("/system-prompts/{prompt_id}", response_model=SystemPromptResponse)
async def update_system_prompt(
    prompt_id: uuid.UUID,
    payload: SystemPromptUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SystemPromptResponse:
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System prompt not found")

    if payload.prompt_name is not None and payload.prompt_name != prompt.prompt_name:
        name_check = await db.execute(
            select(SystemPrompt).where(SystemPrompt.prompt_name == payload.prompt_name)
        )
        if name_check.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A system prompt with this name already exists",
            )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prompt, field, value)

    await db.commit()
    await db.refresh(prompt)
    return SystemPromptResponse.model_validate(prompt)


@router.delete("/system-prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_prompt(
    prompt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System prompt not found")
    await db.delete(prompt)
    await db.commit()


@router.get("/system-prompts/{prompt_id}/versions", response_model=List[SystemPromptVersionResponse])
async def list_prompt_versions(
    prompt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[SystemPromptVersionResponse]:
    prompt_result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    if prompt_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System prompt not found")

    result = await db.execute(
        select(SystemPromptVersion)
        .where(SystemPromptVersion.prompt_id == prompt_id)
        .order_by(SystemPromptVersion.version_number.desc())
    )
    versions = result.scalars().all()
    return [SystemPromptVersionResponse.model_validate(v) for v in versions]


@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def list_audit_logs(
    skip: int = 0,
    limit: int = 20,
    user_id: Optional[uuid.UUID] = None,
    action: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AuditLogResponse]:
    query = select(AuditLog)
    if user_id is not None:
        query = query.where(AuditLog.user_id == user_id)
    if action is not None:
        query = query.where(AuditLog.action == action)
    query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    return [AuditLogResponse.model_validate(log) for log in logs]


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[UserResponse]:
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return [UserResponse.model_validate(u) for u in users]
