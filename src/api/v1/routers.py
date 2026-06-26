from fastapi import APIRouter

from src.modules.user.routers import user_router
from src.modules.auth.router import auth_router
from src.modules.courses.routers import router as courses_router
from src.modules.saude.routers import router as health_router
from src.modules.jobs.routers import jobs_router
from src.modules.orientar.routers import orientar_router
from src.modules.mentorship.routers import router as mentor_router

v1_router = APIRouter(prefix='/v1')


v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(courses_router)
v1_router.include_router(health_router)
v1_router.include_router(jobs_router)
v1_router.include_router(orientar_router)
v1_router.include_router(mentor_router)
