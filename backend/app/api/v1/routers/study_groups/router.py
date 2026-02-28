import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_setup import get_db
from app.models.shared_resource import SharedResource
from app.models.study_group import StudyGroup
from app.models.study_group_member import StudyGroupMember
from app.models.user import User
from app.schemas.shared_resource import SharedResourceCreate, SharedResourceResponse
from app.schemas.study_group import StudyGroupCreate, StudyGroupUpdate, StudyGroupResponse
from app.schemas.study_group_member import StudyGroupMemberResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/study-groups", tags=["Study Groups"])


class JoinRequest(BaseModel):
    invite_code: str


async def _get_group(group_id: uuid.UUID, db: AsyncSession) -> StudyGroup:
    result = await db.execute(select(StudyGroup).where(StudyGroup.id == group_id))
    group = result.scalar_one_or_none()
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study group not found")
    return group


async def _get_membership(
    group_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession
) -> Optional[StudyGroupMember]:
    result = await db.execute(
        select(StudyGroupMember).where(
            StudyGroupMember.group_id == group_id,
            StudyGroupMember.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


@router.get("", response_model=List[StudyGroupResponse])
async def list_groups(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[StudyGroupResponse]:
    result = await db.execute(
        select(StudyGroup)
        .join(StudyGroupMember, StudyGroup.id == StudyGroupMember.group_id)
        .where(StudyGroupMember.user_id == current_user.id)
        .order_by(StudyGroup.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    groups = result.scalars().all()
    return [StudyGroupResponse.model_validate(g) for g in groups]


@router.post("", response_model=StudyGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    payload: StudyGroupCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGroupResponse:
    group = StudyGroup(
        name=payload.name,
        description=payload.description,
        creator_id=current_user.id,
        is_private=payload.is_private,
        invite_code=payload.invite_code,
        max_members=payload.max_members,
    )
    db.add(group)
    await db.flush()

    creator_member = StudyGroupMember(
        group_id=group.id,
        user_id=current_user.id,
        role="creator",
    )
    db.add(creator_member)
    await db.commit()
    await db.refresh(group)
    return StudyGroupResponse.model_validate(group)


@router.get("/{group_id}", response_model=StudyGroupResponse)
async def get_group(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGroupResponse:
    group = await _get_group(group_id, db)
    membership = await _get_membership(group_id, current_user.id, db)
    if membership is None and group.is_private:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return StudyGroupResponse.model_validate(group)


@router.patch("/{group_id}", response_model=StudyGroupResponse)
async def update_group(
    group_id: uuid.UUID,
    payload: StudyGroupUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGroupResponse:
    group = await _get_group(group_id, db)
    if group.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can update this group")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)

    await db.commit()
    await db.refresh(group)
    return StudyGroupResponse.model_validate(group)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    group = await _get_group(group_id, db)
    if group.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can delete this group")
    await db.delete(group)
    await db.commit()


@router.post("/{group_id}/join", response_model=StudyGroupMemberResponse, status_code=status.HTTP_201_CREATED)
async def join_group(
    group_id: uuid.UUID,
    payload: JoinRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyGroupMemberResponse:
    group = await _get_group(group_id, db)

    if group.is_private and group.invite_code != payload.invite_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invite code")

    existing = await _get_membership(group_id, current_user.id, db)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already a member of this group")

    if group.max_members is not None:
        count_result = await db.execute(
            select(StudyGroupMember).where(StudyGroupMember.group_id == group_id)
        )
        current_count = len(count_result.scalars().all())
        if current_count >= group.max_members:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group is full")

    member = StudyGroupMember(
        group_id=group_id,
        user_id=current_user.id,
        role="member",
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return StudyGroupMemberResponse.model_validate(member)


@router.delete("/{group_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_group(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    group = await _get_group(group_id, db)
    if group.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creator cannot leave the group. Transfer ownership or delete the group instead.",
        )

    membership = await _get_membership(group_id, current_user.id, db)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not a member of this group")
    await db.delete(membership)
    await db.commit()


@router.get("/{group_id}/members", response_model=List[StudyGroupMemberResponse])
async def list_members(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[StudyGroupMemberResponse]:
    group = await _get_group(group_id, db)
    membership = await _get_membership(group_id, current_user.id, db)
    if membership is None and group.is_private:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    result = await db.execute(
        select(StudyGroupMember).where(StudyGroupMember.group_id == group_id)
    )
    members = result.scalars().all()
    return [StudyGroupMemberResponse.model_validate(m) for m in members]


@router.delete("/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    group_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    group = await _get_group(group_id, db)
    if group.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can remove members")

    target = await _get_membership(group_id, user_id, db)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    if target.user_id == group.creator_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot remove the group creator")

    await db.delete(target)
    await db.commit()


@router.get("/{group_id}/resources", response_model=List[SharedResourceResponse])
async def list_resources(
    group_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[SharedResourceResponse]:
    group = await _get_group(group_id, db)
    membership = await _get_membership(group_id, current_user.id, db)
    if membership is None and group.is_private:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    result = await db.execute(
        select(SharedResource).where(SharedResource.group_id == group_id)
    )
    resources = result.scalars().all()
    return [SharedResourceResponse.model_validate(r) for r in resources]


@router.post("/{group_id}/resources", response_model=SharedResourceResponse, status_code=status.HTTP_201_CREATED)
async def share_resource(
    group_id: uuid.UUID,
    payload: SharedResourceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SharedResourceResponse:
    await _get_group(group_id, db)
    membership = await _get_membership(group_id, current_user.id, db)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must be a group member to share resources")

    resource = SharedResource(
        group_id=group_id,
        shared_by_user_id=current_user.id,
        resource_type=payload.resource_type,
        resource_id=payload.resource_id,
        title=payload.title,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return SharedResourceResponse.model_validate(resource)


@router.delete("/{group_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    group_id: uuid.UUID,
    resource_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    group = await _get_group(group_id, db)

    result = await db.execute(
        select(SharedResource).where(
            SharedResource.id == resource_id,
            SharedResource.group_id == group_id,
        )
    )
    resource = result.scalar_one_or_none()
    if resource is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    if resource.shared_by_user_id != current_user.id and group.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to remove this resource")

    await db.delete(resource)
    await db.commit()
