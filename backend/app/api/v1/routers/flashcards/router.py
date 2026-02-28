import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.flashcard import Flashcard
from app.models.flashcard_deck import FlashcardDeck
from app.models.flashcard_review import FlashcardReview
from app.models.tag import Tag
from app.models.user import User
from app.schemas.flashcard import FlashcardCreate, FlashcardUpdate, FlashcardResponse
from app.schemas.flashcard_review import FlashcardReviewCreate, FlashcardReviewResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])


class TagIdsRequest(BaseModel):
    tag_ids: List[uuid.UUID]


async def _get_card_owned_by_user(
    card_id: uuid.UUID, current_user: User, db: AsyncSession
) -> Flashcard:
    result = await db.execute(
        select(Flashcard)
        .join(FlashcardDeck, Flashcard.deck_id == FlashcardDeck.id)
        .where(Flashcard.id == card_id, FlashcardDeck.user_id == current_user.id)
    )
    card = result.scalar_one_or_none()
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")
    return card


@router.get("/due", response_model=List[FlashcardResponse])
async def list_due_cards(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[FlashcardResponse]:
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Flashcard)
        .join(FlashcardDeck, Flashcard.deck_id == FlashcardDeck.id)
        .where(
            FlashcardDeck.user_id == current_user.id,
            Flashcard.is_suspended == False,  # noqa: E712
            (Flashcard.next_review_date.is_(None)) | (Flashcard.next_review_date <= now),
        )
        .offset(skip)
        .limit(limit)
    )
    cards = result.scalars().all()
    return [FlashcardResponse.model_validate(c) for c in cards]


@router.post("", response_model=FlashcardResponse, status_code=status.HTTP_201_CREATED)
async def create_flashcard(
    payload: FlashcardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardResponse:
    deck_result = await db.execute(
        select(FlashcardDeck).where(
            FlashcardDeck.id == payload.deck_id,
            FlashcardDeck.user_id == current_user.id,
        )
    )
    deck = deck_result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard deck not found")

    card = Flashcard(
        deck_id=payload.deck_id,
        front_content=payload.front_content,
        back_content=payload.back_content,
        front_content_type=payload.front_content_type,
        back_content_type=payload.back_content_type,
        hint=payload.hint,
        explanation=payload.explanation,
        difficulty_rating=payload.difficulty_rating,
    )
    db.add(card)
    deck.total_cards = (deck.total_cards or 0) + 1
    await db.commit()
    await db.refresh(card)
    return FlashcardResponse.model_validate(card)


@router.get("/{card_id}", response_model=FlashcardResponse)
async def get_flashcard(
    card_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardResponse:
    card = await _get_card_owned_by_user(card_id, current_user, db)
    return FlashcardResponse.model_validate(card)


@router.patch("/{card_id}", response_model=FlashcardResponse)
async def update_flashcard(
    card_id: uuid.UUID,
    payload: FlashcardUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardResponse:
    card = await _get_card_owned_by_user(card_id, current_user, db)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)

    await db.commit()
    await db.refresh(card)
    return FlashcardResponse.model_validate(card)


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flashcard(
    card_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    card = await _get_card_owned_by_user(card_id, current_user, db)

    deck_result = await db.execute(
        select(FlashcardDeck).where(FlashcardDeck.id == card.deck_id)
    )
    deck = deck_result.scalar_one_or_none()
    if deck is not None and deck.total_cards > 0:
        deck.total_cards -= 1

    await db.delete(card)
    await db.commit()


@router.post("/{card_id}/review", response_model=FlashcardReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    card_id: uuid.UUID,
    payload: FlashcardReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardReviewResponse:
    card = await _get_card_owned_by_user(card_id, current_user, db)

    review = FlashcardReview(
        flashcard_id=card.id,
        user_id=current_user.id,
        session_id=payload.session_id,
        quality_rating=payload.quality_rating,
        response_time_seconds=payload.response_time_seconds,
        previous_ease_factor=payload.previous_ease_factor,
        new_ease_factor=payload.new_ease_factor,
        previous_interval=payload.previous_interval,
        new_interval=payload.new_interval,
    )
    db.add(review)
    card.total_reviews = (card.total_reviews or 0) + 1
    if payload.quality_rating is not None and payload.quality_rating >= 3:
        card.correct_reviews = (card.correct_reviews or 0) + 1

    await db.commit()
    await db.refresh(review)
    return FlashcardReviewResponse.model_validate(review)


@router.get("/{card_id}/reviews", response_model=List[FlashcardReviewResponse])
async def list_reviews(
    card_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[FlashcardReviewResponse]:
    card = await _get_card_owned_by_user(card_id, current_user, db)
    result = await db.execute(
        select(FlashcardReview)
        .where(FlashcardReview.flashcard_id == card.id, FlashcardReview.user_id == current_user.id)
        .order_by(FlashcardReview.reviewed_at.desc())
    )
    reviews = result.scalars().all()
    return [FlashcardReviewResponse.model_validate(r) for r in reviews]


@router.post("/{card_id}/tags", response_model=FlashcardResponse)
async def add_tags_to_flashcard(
    card_id: uuid.UUID,
    payload: TagIdsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardResponse:
    card = await _get_card_owned_by_user(card_id, current_user, db)

    for tag_id in payload.tag_ids:
        tag_result = await db.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
        )
        tag = tag_result.scalar_one_or_none()
        if tag is not None and tag not in card.tags:
            card.tags.append(tag)

    await db.commit()
    await db.refresh(card)
    return FlashcardResponse.model_validate(card)
