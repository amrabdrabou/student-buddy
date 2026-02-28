import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.study_subject import StudySubject
from app.models.user import User
from app.schemas.study_subject import StudySubjectCreate, StudySubjectUpdate, StudySubjectResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("", response_model=List[StudySubjectResponse])
async def list_subjects(
    skip: int = 0,
    limit: int = 20,
    is_archived: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[StudySubjectResponse]:
    query = select(StudySubject).where(StudySubject.user_id == current_user.id)
    if is_archived is not None:
        query = query.where(StudySubject.is_archived == is_archived)
    query = query.order_by(StudySubject.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    subjects = result.scalars().all()
    return [StudySubjectResponse.model_validate(s) for s in subjects]


@router.post("", response_model=StudySubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    payload: StudySubjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySubjectResponse:
    subject = StudySubject(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        color_hex=payload.color_hex,
        is_archived=payload.is_archived,
    )
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return StudySubjectResponse.model_validate(subject)


@router.get("/{subject_id}", response_model=StudySubjectResponse)
async def get_subject(
    subject_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySubjectResponse:
    result = await db.execute(
        select(StudySubject).where(
            StudySubject.id == subject_id,
            StudySubject.user_id == current_user.id,
        )
    )
    subject = result.scalar_one_or_none()
    if subject is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return StudySubjectResponse.model_validate(subject)


@router.patch("/{subject_id}", response_model=StudySubjectResponse)
async def update_subject(
    subject_id: uuid.UUID,
    payload: StudySubjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudySubjectResponse:
    result = await db.execute(
        select(StudySubject).where(
            StudySubject.id == subject_id,
            StudySubject.user_id == current_user.id,
        )
    )
    subject = result.scalar_one_or_none()
    if subject is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subject, field, value)

    await db.commit()
    await db.refresh(subject)
    return StudySubjectResponse.model_validate(subject)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(
    subject_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(StudySubject).where(
            StudySubject.id == subject_id,
            StudySubject.user_id == current_user.id,
        )
    )
    subject = result.scalar_one_or_none()
    if subject is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    await db.delete(subject)
    await db.commit()
