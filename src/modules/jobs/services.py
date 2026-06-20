from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Jobs
from .schemas import JobCreate, JobUpdate


def calculate_match(user_techs: list[str], job_techs: list[str]) -> int:
    if not job_techs:
        return 100

    intersection = set(user_techs).intersection(job_techs)
    return int((len(intersection) / len(job_techs)) * 100)


async def get_matching_jobs(
    session: AsyncSession, user_area: str, user_techs: list[str]
):
    query = select(Jobs).where(Jobs.tech_area == user_area)
    result = await session.execute(query)
    jobs = result.scalars().all()

    matched_jobs = [
        {
            'job_details': job,
            'match_percentage': calculate_match(
                user_techs, job.require_techs
            ),
        }
        for job in jobs
    ]

    return sorted(
        matched_jobs, key=lambda x: x['match_percentage'], reverse=True
    )


async def create_job(session: AsyncSession, job_in: JobCreate) -> Jobs:
    new_job = Jobs(**job_in.model_dump())
    session.add(new_job)
    await session.commit()
    await session.refresh(new_job)
    return new_job


async def get_job_by_id(session: AsyncSession, job_id: int) -> Jobs | None:
    result = await session.execute(select(Jobs).where(Jobs.id == job_id))
    return result.scalar_one_or_none()


async def update_job(
    session: AsyncSession, job_id: int, job_in: JobUpdate
) -> Jobs | None:
    job = await get_job_by_id(session, job_id)
    if not job:
        return None

    update_data = job_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    await session.commit()
    await session.refresh(job)
    return job


async def delete_job(session: AsyncSession, job_id: int) -> bool:
    job = await get_job_by_id(session, job_id)
    if not job:
        return False

    await session.delete(job)
    await session.commit()
    return True
