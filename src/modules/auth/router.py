from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import Token
from src.core.database import get_db
from src.core.exceptions import Unauthorized
from src.core.security import (
    authenticate_user_service,
    create_access_token,
)

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    user = await authenticate_user_service(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise Unauthorized('Incorrect username or password')

    access_token = create_access_token(data={'sub': user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }