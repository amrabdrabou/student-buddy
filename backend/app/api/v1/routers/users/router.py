from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.models.ai_usage_stats import AiUsageStats
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.user_preferences import (
    UserPreferencesCreate,
    UserPreferencesUpdate,
    UserPreferencesResponse,
)
from app.schemas.ai_usage_stats import AiUsageStatsResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await db.delete(current_user)
    await db.commit()


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserPreferencesResponse:
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    )
    prefs = result.scalar_one_or_none()
    if prefs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")
    return UserPreferencesResponse.model_validate(prefs)


@router.put("/me/preferences", response_model=UserPreferencesResponse)
async def upsert_preferences(
    payload: UserPreferencesCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserPreferencesResponse:
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    )
    prefs = result.scalar_one_or_none()
    if prefs is None:
        prefs = UserPreferences(user_id=current_user.id)
        db.add(prefs)

    data = payload.model_dump(exclude={"user_id"})
    for field, value in data.items():
        setattr(prefs, field, value)

    await db.commit()
    await db.refresh(prefs)
    return UserPreferencesResponse.model_validate(prefs)


@router.patch("/me/preferences", response_model=UserPreferencesResponse)
async def patch_preferences(
    payload: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserPreferencesResponse:
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    )
    prefs = result.scalar_one_or_none()
    if prefs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prefs, field, value)

    await db.commit()
    await db.refresh(prefs)
    return UserPreferencesResponse.model_validate(prefs)


@router.get("/me/usage-stats", response_model=List[AiUsageStatsResponse])
async def get_usage_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AiUsageStatsResponse]:
    result = await db.execute(
        select(AiUsageStats)
        .where(AiUsageStats.user_id == current_user.id)
        .order_by(AiUsageStats.stat_date.desc())
    )
    stats = result.scalars().all()
    return [AiUsageStatsResponse.model_validate(s) for s in stats]
