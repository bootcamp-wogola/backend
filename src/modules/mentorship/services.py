# app/services/mentorship_service.py

from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Mentorship, MentorshipType, MentorshipStatus
from schemas import MentorshipCreate, MentorshipUpdate


async def create_mentorship(
    db: AsyncSession,
    payload: MentorshipCreate,
    mentor_id: int,
) -> Mentorship:
    mentorship = Mentorship(
        **payload.model_dump(exclude={"mentor_id"}),
        mentor_id=mentor_id,
    )
    db.add(mentorship)
    await db.commit()
    await db.refresh(mentorship)
    return mentorship


async def list_mentorships(
    db: AsyncSession,
    type: Optional[MentorshipType] = None,
    status_filter: Optional[MentorshipStatus] = None,
    mentor_id: Optional[int] = None,
) -> Sequence[Mentorship]:
    query = select(Mentorship)

    if type is not None:
        query = query.where(Mentorship.type == type)
    if status_filter is not None:
        query = query.where(Mentorship.status == status_filter)
    if mentor_id is not None:
        query = query.where(Mentorship.mentor_id == mentor_id)

    result = await db.execute(query)
    return result.scalars().all()


async def get_mentorship_or_404(db: AsyncSession, mentorship_id: int) -> Mentorship:
    mentorship = await db.get(Mentorship, mentorship_id)
    if not mentorship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentorship not found")
    return mentorship


def ensure_owner(mentorship: Mentorship, current_user_id: int) -> None:
    if mentorship.mentor_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this mentorship",
        )


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