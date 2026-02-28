import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.flashcard import Flashcard
from app.models.flashcard_deck import FlashcardDeck
from app.models.user import User
from app.schemas.flashcard import FlashcardResponse
from app.schemas.flashcard_deck import FlashcardDeckCreate, FlashcardDeckUpdate, FlashcardDeckResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/flashcard-decks", tags=["Flashcard Decks"])


@router.get("", response_model=List[FlashcardDeckResponse])
async def list_decks(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[uuid.UUID] = None,
    is_archived: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[FlashcardDeckResponse]:
    query = select(FlashcardDeck).where(FlashcardDeck.user_id == current_user.id)
    if subject_id is not None:
        query = query.where(FlashcardDeck.subject_id == subject_id)
    if is_archived is not None:
        query = query.where(FlashcardDeck.is_archived == is_archived)
    query = query.order_by(FlashcardDeck.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    decks = result.scalars().all()
    return [FlashcardDeckResponse.model_validate(d) for d in decks]


@router.post("", response_model=FlashcardDeckResponse, status_code=status.HTTP_201_CREATED)
async def create_deck(
    payload: FlashcardDeckCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardDeckResponse:
    deck = FlashcardDeck(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        title=payload.title,
        description=payload.description,
        is_public=payload.is_public,
        is_archived=payload.is_archived,
    )
    db.add(deck)
    await db.commit()
    await db.refresh(deck)
    return FlashcardDeckResponse.model_validate(deck)


@router.get("/{deck_id}", response_model=FlashcardDeckResponse)
async def get_deck(
    deck_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardDeckResponse:
    result = await db.execute(
        select(FlashcardDeck).where(
            FlashcardDeck.id == deck_id,
            FlashcardDeck.user_id == current_user.id,
        )
    )
    deck = result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard deck not found")
    return FlashcardDeckResponse.model_validate(deck)


@router.patch("/{deck_id}", response_model=FlashcardDeckResponse)
async def update_deck(
    deck_id: uuid.UUID,
    payload: FlashcardDeckUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FlashcardDeckResponse:
    result = await db.execute(
        select(FlashcardDeck).where(
            FlashcardDeck.id == deck_id,
            FlashcardDeck.user_id == current_user.id,
        )
    )
    deck = result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard deck not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deck, field, value)

    await db.commit()
    await db.refresh(deck)
    return FlashcardDeckResponse.model_validate(deck)


@router.delete("/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deck(
    deck_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(FlashcardDeck).where(
            FlashcardDeck.id == deck_id,
            FlashcardDeck.user_id == current_user.id,
        )
    )
    deck = result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard deck not found")
    await db.delete(deck)
    await db.commit()


@router.get("/{deck_id}/cards", response_model=List[FlashcardResponse])
async def list_deck_cards(
    deck_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
    is_suspended: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[FlashcardResponse]:
    deck_result = await db.execute(
        select(FlashcardDeck).where(
            FlashcardDeck.id == deck_id,
            FlashcardDeck.user_id == current_user.id,
        )
    )
    deck = deck_result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard deck not found")

    query = select(Flashcard).where(Flashcard.deck_id == deck_id)
    if is_suspended is not None:
        query = query.where(Flashcard.is_suspended == is_suspended)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    cards = result.scalars().all()
    return [FlashcardResponse.model_validate(c) for c in cards]
