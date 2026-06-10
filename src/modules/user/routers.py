from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import Conflict, Forbidden, NotFound
from src.core.security import get_current_user
from . import services
from .model import User
from .schemas import UserCreate, UserGet, UserUpdate


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('/{user_id}', response_model=UserGet)
async def read_user(
	user_id: int,
	session: AsyncSession = Depends(get_db),
):
	user = await services.get_user_by_id(session, user_id)
	if not user:
		raise NotFound('User not found')

	return user


@user_router.post('/', response_model=UserGet, status_code=201)
async def create_user(
	user_in: UserCreate,
	session: AsyncSession = Depends(get_db),
):
	user = await services.create_user(session, user_in)
	if not user:
		raise Conflict('Username or email already exists')

	return user


@user_router.patch('/{user_id}', response_model=UserGet)
async def update_user(
	user_id: int,
	user_in: UserUpdate,
	session: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user),
):
	if current_user.id != user_id:
		raise Forbidden('User can only modify own account')

	try:
		user = await services.update_user(session, user_id, user_in)
	except ValueError as exc:
		raise Conflict(str(exc))

	if not user:
		raise NotFound('User not found')

	return user


@user_router.delete('/{user_id}', status_code=204)
async def delete_user(
	user_id: int,
	session: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user),
):
	if current_user.id != user_id:
		raise Forbidden('User can only modify own account')

	user = await services.delete_user(session, user_id)
	if not user:
		raise NotFound('User not found')

	return None
