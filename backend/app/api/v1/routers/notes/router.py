import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.note import Note
from app.models.tag import Tag
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])


class TagIdsRequest(BaseModel):
    tag_ids: List[uuid.UUID]


@router.get("", response_model=List[NoteResponse])
async def list_notes(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[uuid.UUID] = None,
    is_archived: Optional[bool] = None,
    is_pinned: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[NoteResponse]:
    query = select(Note).where(Note.user_id == current_user.id)
    if subject_id is not None:
        query = query.where(Note.subject_id == subject_id)
    if is_archived is not None:
        query = query.where(Note.is_archived == is_archived)
    if is_pinned is not None:
        query = query.where(Note.is_pinned == is_pinned)
    query = query.order_by(Note.updated_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return [NoteResponse.model_validate(n) for n in notes]


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    note = Note(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        title=payload.title,
        content=payload.content,
        content_format=payload.content_format,
        summary=payload.summary,
        key_concepts=payload.key_concepts,
        is_pinned=payload.is_pinned,
        is_archived=payload.is_archived,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return NoteResponse.model_validate(note)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteResponse.model_validate(note)


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: uuid.UUID,
    payload: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)

    await db.commit()
    await db.refresh(note)
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    await db.delete(note)
    await db.commit()


@router.post("/{note_id}/tags", response_model=NoteResponse)
async def add_tags_to_note(
    note_id: uuid.UUID,
    payload: TagIdsRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    for tag_id in payload.tag_ids:
        tag_result = await db.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id)
        )
        tag = tag_result.scalar_one_or_none()
        if tag is not None and tag not in note.tags:
            note.tags.append(tag)

    await db.commit()
    await db.refresh(note)
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}/tags/{tag_id}", response_model=NoteResponse)
async def remove_tag_from_note(
    note_id: uuid.UUID,
    tag_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    tag_result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = tag_result.scalar_one_or_none()
    if tag is not None and tag in note.tags:
        note.tags.remove(tag)

    await db.commit()
    await db.refresh(note)
    return NoteResponse.model_validate(note)
