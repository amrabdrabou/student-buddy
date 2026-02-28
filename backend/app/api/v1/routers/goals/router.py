import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.study_goal import StudyGoal
from app.models.user import User
from app.schemas.study_goal import StudyGoalCreate, StudyGoalUpdate, StudyGoalResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/goals", tags=["Study Goals"])


@router.get("", response_model=List[StudyGoalResponse])
async def list_goals(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[uuid.UUID] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[StudyGoalResponse]:
    query = select(StudyGoal).where(StudyGoal.user_id == current_user.id)
    if subject_id is not None:
        query = query.where(StudyGoal.subject_id == subject_id)
    if is_active is not None:
        query = query.where(StudyGoal.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    goals = result.scalars().all()
    return [StudyGoalResponse.model_validate(g) for g in goals]


@router.post("", response_model=StudyGoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    payload: StudyGoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGoalResponse:
    goal = StudyGoal(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        goal_type=payload.goal_type,
        target_value=payload.target_value,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_active=payload.is_active,
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return StudyGoalResponse.model_validate(goal)


@router.get("/{goal_id}", response_model=StudyGoalResponse)
async def get_goal(
    goal_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGoalResponse:
    result = await db.execute(
        select(StudyGoal).where(
            StudyGoal.id == goal_id,
            StudyGoal.user_id == current_user.id,
        )
    )
    goal = result.scalar_one_or_none()
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return StudyGoalResponse.model_validate(goal)


@router.patch("/{goal_id}", response_model=StudyGoalResponse)
async def update_goal(
    goal_id: uuid.UUID,
    payload: StudyGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGoalResponse:
    result = await db.execute(
        select(StudyGoal).where(
            StudyGoal.id == goal_id,
            StudyGoal.user_id == current_user.id,
        )
    )
    goal = result.scalar_one_or_none()
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)

    await db.commit()
    await db.refresh(goal)
    return StudyGoalResponse.model_validate(goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(StudyGoal).where(
            StudyGoal.id == goal_id,
            StudyGoal.user_id == current_user.id,
        )
    )
    goal = result.scalar_one_or_none()
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    await db.delete(goal)
    await db.commit()
