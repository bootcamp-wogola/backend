from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import NotFound
from src.core.security import get_current_user
from src.modules.user.models import User
from src.modules.user.services import get_full_user

from . import services
from .schemas import JobCreate, JobUpdate, JobResponse, JobMatchResponse

jobs_router = APIRouter(prefix='/jobs', tags=['Jobs'])


@jobs_router.get('/matching', response_model=list[JobMatchResponse])
async def get_matching_jobs(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    full_user = await get_full_user(session, current_user)

    if not full_user or not full_user.professional_profile:
        raise NotFound('Professional profile incomplete.')

    matched_jobs = await services.get_matching_jobs(
        session,
        user_area=full_user.professional_profile.tech_area,
        user_techs=full_user.professional_profile.technologies
    )
    
    return matched_jobs


@jobs_router.post('/', response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await services.create_job(session, job_in)


@jobs_router.patch('/{job_id}', response_model=JobResponse)
async def update_job(
    job_id: int,
    job_in: JobUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = await services.update_job(session, job_id, job_in)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    return job


@jobs_router.delete('/{job_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await services.delete_job(session, job_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')