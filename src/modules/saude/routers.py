from fastapi import APIRouter
from . import services, schemas

router = APIRouter(prefix='/saude', tags=['Saude'])


@router.post('/', status_code=200, response_model=schemas.SaudeResponse)
async def checkin(
    payload: schemas.SaudeRequest,
):
    return await services.processar_checkin(payload)
