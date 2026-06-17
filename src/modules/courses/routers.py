from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import services, schemas
from src.core.database import get_db
from src.core.security import get_current_user

router = APIRouter(prefix='/courses', tags=['Courses'])

# TODO: Better responses


# GET
@router.get('/', status_code=200)
async def get_all(session: AsyncSession = Depends(get_db)):
    courses = await services.get_all_courses(session)
    return courses


@router.get('/by-tech', status_code=200)
async def get_by_tech(
    techs: list[str] = Query(...), session: AsyncSession = Depends(get_db)
):
    courses = await services.get_by_tech(session, techs)
    return courses


@router.get('/by_provider', status_code=200)
async def get_by_provider(
    providers: list[str] = Query(...), session: AsyncSession = Depends(get_db)
):
    response = await services.get_by_provider(session, providers)
    return response


@router.get('/{course_id}', status_code=200)
async def get_by_id(course_id: int, session: AsyncSession = Depends(get_db)):
    course = await services.get_course_by_id(session, course_id)
    return course


# POST
@router.post('/', status_code=201)
async def create(
    course_in: schemas.CourseCreate,
    user=Depends(get_current_user),
    session=Depends(get_db),
):
    course = await services.create_course(session, course_in)
    return course
