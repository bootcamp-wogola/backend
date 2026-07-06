from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_current_user
from src.core.database import get_db
from src.modules.user.models import User
from . import services, schemas

router = APIRouter(prefix='/saude', tags=['Saude'])


@router.post('/', status_code=200, response_model=schemas.HealthResponse)
async def checkin(
    payload: schemas.HealthRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    return await services.processar_checkin(payload, current_user, session)
