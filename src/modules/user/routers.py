from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exceptions import Conflict, Forbidden, NotFound
from src.core.security import get_current_user
from . import services
from .models import User
from .schemas import UserCreate, UserGet, UserUpdate, ProfessionalDataUpdate, ProfessionalDataGet, ProfessionalDataBase


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


@user_router.get('/{user_id}/professional', response_model=ProfessionalDataGet)
async def read_professional(
	user_id: int,
	session: AsyncSession = Depends(get_db)
):
	professional = await services.get_professional_by_id(session, user_id)
	if not professional:
		raise NotFound('User Professional data not found')
	return professional


@user_router.post('/', response_model=UserGet, status_code=201)
async def create_user(
	user_in: UserCreate,
	session: AsyncSession = Depends(get_db),
):
	user = await services.create_user(session, user_in)
	if not user:
		raise Conflict('Username or email already exists')

	return user

@user_router.post('/{user_id}/professional', status_code=201, response_model=ProfessionalDataGet)
async def create_professional(
	user_id: int,
	professional_in: ProfessionalDataBase,
	session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	if current_user.id != user_id:
		raise Forbidden('User can only modify own account')

	try:
		new_profile = await services.create_professional_profile(session, user_id, professional_in)
		return new_profile
	
	except ValueError as exc:
		raise HTTPException(status_code=409, detail=str(exc))


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

@user_router.patch('/{user_id}/professional', response_model=ProfessionalDataGet)
async def update_professional(
	user_id : int,
	professional_in : ProfessionalDataUpdate,
	session = Depends(get_db),
	current_user = Depends(get_current_user)
):
	if current_user.id != user_id:
		raise Forbidden('User can only modify own account')

	
	update = await services.update_professional_data(session, user_id, professional_in)
	
	if not update:
		raise NotFound('Professional profile not found')
	
	return update


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
