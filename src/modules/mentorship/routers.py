from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from .models import MentorshipType, MentorshipStatus
from .schemas import (
    MentorshipCreate,
    MentorshipUpdate,
    MentorshipResponse,
)
from . import services

router = APIRouter(prefix='/mentorships', tags=['mentorships'])


@router.post(
    '', response_model=MentorshipResponse, status_code=status.HTTP_201_CREATED
)
async def create_mentorship(
    payload: MentorshipCreate,
    db: AsyncSession = Depends(get_db),
):
    return await services.create_mentorship(db, payload)


@router.get('', response_model=list[MentorshipResponse])
async def list_mentorships(
    type: Optional[MentorshipType] = None,
    status_filter: Optional[MentorshipStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    return await services.list_mentorship(db, type, status_filter)


@router.get('/{mentorship_id}', response_model=MentorshipResponse)
async def get_mentorship(
    mentorship_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_mentorship_or_404(db, mentorship_id)


@router.patch('/{mentorship_id}', response_model=MentorshipResponse)
async def update_mentorship(
    mentorship_id: int,
    payload: MentorshipUpdate,
    db: AsyncSession = Depends(get_db),
):
    mentorship = await services.get_mentorship_or_404(db, mentorship_id)
    return await services.update_mentorship(db, mentorship, payload)


@router.delete('/{mentorship_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_mentorship(
    mentorship_id: int,
    db: AsyncSession = Depends(get_db),
):
    mentorship = await services.get_mentorship_or_404(db, mentorship_id)
    await services.delete_mentorship(db, mentorship)
