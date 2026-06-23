# app/routers/mentorship.py

from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import get_current_user
from ..user.models import User
from models import MentorshipType, MentorshipStatus
from schemas import (
    MentorshipCreate,
    MentorshipUpdate,
    MentorshipResponse,
)
from . import services


router = APIRouter(prefix="/mentorships", tags=["mentorships"])


@router.post("", response_model=MentorshipResponse, status_code=status.HTTP_201_CREATED)
async def create_mentorship(
    payload: MentorshipCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.create_mentorship(db, payload, mentor_id=current_user.id)


@router.get("", response_model=list[MentorshipResponse])
async def list_mentorships(
    type: Optional[MentorshipType] = None,
    status_filter: Optional[MentorshipStatus] = None,
    mentor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    return await services.list_mentorships(db, type, status_filter, mentor_id)


@router.get("/{mentorship_id}", response_model=MentorshipResponse)
async def get_mentorship(
    mentorship_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_mentorship_or_404(db, mentorship_id)


@router.patch("/{mentorship_id}", response_model=MentorshipResponse)
async def update_mentorship(
    mentorship_id: int,
    payload: MentorshipUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mentorship = await services.get_mentorship_or_404(db, mentorship_id)
    services.ensure_owner(mentorship, current_user.id)
    return await services.update_mentorship(db, mentorship, payload)


@router.delete("/{mentorship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mentorship(
    mentorship_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mentorship = await services.get_mentorship_or_404(db, mentorship_id)
    services.ensure_owner(mentorship, current_user.id)
    await services.delete_mentorship(db, mentorship)