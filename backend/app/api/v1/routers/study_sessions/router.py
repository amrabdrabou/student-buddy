import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.study_session import StudySession
from app.models.user import User
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate, StudySessionResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


@router.get("", response_model=List[StudySessionResponse])
async def list_sessions(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[uuid.UUID] = None,
    session_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[StudySessionResponse]:
    query = select(StudySession).where(StudySession.user_id == current_user.id)
    if subject_id is not None:
        query = query.where(StudySession.subject_id == subject_id)
    if session_type is not None:
        query = query.where(StudySession.session_type == session_type)
    query = query.order_by(StudySession.started_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    sessions = result.scalars().all()
    return [StudySessionResponse.model_validate(s) for s in sessions]


@router.post("", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: StudySessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySessionResponse:
    session = StudySession(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        session_type=payload.session_type,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return StudySessionResponse.model_validate(session)


@router.get("/{session_id}", response_model=StudySessionResponse)
async def get_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySessionResponse:
    result = await db.execute(
        select(StudySession).where(
            StudySession.id == session_id,
            StudySession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study session not found")
    return StudySessionResponse.model_validate(session)


@router.patch("/{session_id}", response_model=StudySessionResponse)
async def update_session(
    session_id: uuid.UUID,
    payload: StudySessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySessionResponse:
    result = await db.execute(
        select(StudySession).where(
            StudySession.id == session_id,
            StudySession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study session not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)

    await db.commit()
    await db.refresh(session)
    return StudySessionResponse.model_validate(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(StudySession).where(
            StudySession.id == session_id,
            StudySession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study session not found")
    await db.delete(session)
    await db.commit()


@router.post("/{session_id}/complete", response_model=StudySessionResponse)
async def complete_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySessionResponse:
    result = await db.execute(
        select(StudySession).where(
            StudySession.id == session_id,
            StudySession.user_id == current_user.id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study session not found")

    now = datetime.now(timezone.utc)
    session.is_completed = True
    session.ended_at = now

    if session.started_at is not None:
        started = session.started_at
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        duration_seconds = (now - started).total_seconds()
        session.duration_minutes = int(duration_seconds / 60)

    await db.commit()
    await db.refresh(session)
    return StudySessionResponse.model_validate(session)
