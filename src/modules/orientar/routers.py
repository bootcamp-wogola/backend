from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.security import get_current_user
from src.modules.user.models import User

from . import services
from .schemas import OrientarResponse

orientar_router = APIRouter(prefix='/orientar', tags=['Orientar'])


@orientar_router.post('/', status_code=200, response_model=OrientarResponse)
async def orientar(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.gerar_orientacao(session, current_user)