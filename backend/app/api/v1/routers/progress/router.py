from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.daily_progress import DailyProgress
from app.models.user import User
from app.schemas.daily_progress import DailyProgressCreate, DailyProgressUpdate, DailyProgressResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/daily", response_model=List[DailyProgressResponse])
async def list_daily_progress(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[DailyProgressResponse]:
    result = await db.execute(
        select(DailyProgress)
        .where(DailyProgress.user_id == current_user.id)
        .order_by(DailyProgress.date.desc())
        .offset(skip)
        .limit(limit)
    )
    records = result.scalars().all()
    return [DailyProgressResponse.model_validate(r) for r in records]


@router.get("/daily/{progress_date}", response_model=DailyProgressResponse)
async def get_daily_progress(
    progress_date: date,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DailyProgressResponse:
    result = await db.execute(
        select(DailyProgress).where(
            DailyProgress.user_id == current_user.id,
            DailyProgress.date == progress_date,
        )
    )
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily progress not found for this date")
    return DailyProgressResponse.model_validate(record)


@router.post("/daily", response_model=DailyProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_progress(
    payload: DailyProgressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DailyProgressResponse:
    existing = await db.execute(
        select(DailyProgress).where(
            DailyProgress.user_id == current_user.id,
            DailyProgress.date == payload.date,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Daily progress for this date already exists",
        )

    record = DailyProgress(
        user_id=current_user.id,
        date=payload.date,
        total_study_minutes=payload.total_study_minutes,
        cards_reviewed=payload.cards_reviewed,
        cards_mastered=payload.cards_mastered,
        notes_created=payload.notes_created,
        streak_days=payload.streak_days,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return DailyProgressResponse.model_validate(record)


@router.patch("/daily/{progress_date}", response_model=DailyProgressResponse)
async def update_daily_progress(
    progress_date: date,
    payload: DailyProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DailyProgressResponse:
    result = await db.execute(
        select(DailyProgress).where(
            DailyProgress.user_id == current_user.id,
            DailyProgress.date == progress_date,
        )
    )
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily progress not found for this date")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    await db.commit()
    await db.refresh(record)
    return DailyProgressResponse.model_validate(record)


@router.get("/streak")
async def get_streak(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(DailyProgress)
        .where(DailyProgress.user_id == current_user.id)
        .order_by(DailyProgress.date.desc())
        .limit(365)
    )
    records = result.scalars().all()

    if not records:
        return {"streak_days": 0, "last_study_date": None}

    last_study_date: Optional[date] = records[0].date
    streak = 0
    check_date = date.today()

    for record in records:
        if record.date == check_date:
            if record.total_study_minutes > 0:
                streak += 1
                check_date = check_date - timedelta(days=1)
            else:
                break
        elif record.date == check_date - timedelta(days=1):
            check_date = check_date - timedelta(days=1)
            if record.total_study_minutes > 0:
                streak += 1
                check_date = check_date - timedelta(days=1)
            else:
                break
        else:
            break

    return {"streak_days": streak, "last_study_date": last_study_date}
