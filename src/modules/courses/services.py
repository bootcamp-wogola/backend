from sqlalchemy import select
from .model import Courses


async def get_all_courses(db):
    courses = await db.scalars(select(Courses))
    return courses.all()


async def get_course_by_id(db, identifier: int):
    return await db.get(Courses, identifier)


async def get_by_tech(db, tecnologies: list[str]):
    result = await db.scalars(
        select(Courses).where(Courses.tecnologies.overlap(tecnologies))
    )
    return result.all()


async def get_by_provider(db, providers: list[str]):
    result = await db.scalars(
        select(Courses).where(Courses.provider.in_(providers))
    )
    return result.all()


async def create_course(db, course):
    # Convert to string because HttpUrl is not directly comparable to string in the database
    link_url = str(course.link)

    duplicate_course = await db.scalar(
        select(Courses).where(
            (Courses.name == course.name)
            | (Courses.link == link_url)
            | (Courses.provider == course.provider)
        )
    )

    if duplicate_course:
        return None

    data = course.model_dump()
    data['link'] = link_url

    new_course = Courses(**data)

    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    return new_course
