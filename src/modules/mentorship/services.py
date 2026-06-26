# app/services/mentorship_service.py
from typing import Optional, Sequence
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Mentorship, MentorshipType, MentorshipStatus
from .schemas import MentorshipCreate, MentorshipUpdate


async def create_mentorship(
    db: AsyncSession,
    payload: MentorshipCreate,
) -> Mentorship:
    mentorship = Mentorship(**payload.model_dump())
    db.add(mentorship)

    await db.commit()
    await db.refresh(mentorship)
    return mentorship


async def list_mentorship(
    db: AsyncSession,
    mentorship_type: Optional[MentorshipType] = None,
    status_filter: Optional[MentorshipStatus] = None,
) -> Sequence[Mentorship]:
    query = select(Mentorship)
    if mentorship_type is not None:
        query = query.where(Mentorship.type == mentorship_type)
    if status_filter is not None:
        query = query.where(Mentorship.status == status_filter)
    result = await db.execute(query)
    return result.scalars().all()


async def get_mentorship_or_404(
    db: AsyncSession, mentorship_id: int
) -> type[Mentorship]:
    mentorship = await db.get(Mentorship, mentorship_id)
    if not mentorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Mentorship not found',
        )
    return mentorship


async def update_mentorship(
    db: AsyncSession,
    mentorship: Mentorship,
    payload: MentorshipUpdate,
) -> Mentorship:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(mentorship, field, value)
    await db.commit()
    await db.refresh(mentorship)
    return mentorship


async def delete_mentorship(db: AsyncSession, mentorship: Mentorship) -> None:
    await db.delete(mentorship)
    await db.commit()
