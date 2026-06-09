from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import services, schemas
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/courses", tags=['Courses'])

@router.get("/", status_code=200)
async def get_all(
    session: AsyncSession = Depends(get_db)
):
    courses = await services.get_all_courses(session)
    return courses


@router.get("/{course_id}", status_code=200)
async def get_by_id(
    course_id: int,
    session: AsyncSession = Depends(get_db)
):
    course = await services.get_course_by_id(session, course_id)
    return course


@router.post("/", status_code=201)
async def create(
    course_in : schemas.CourseCreate,
    user = Depends(get_current_user),
    session = Depends(get_db),
):
    course = await services.create_course(session, course_in)
    return course