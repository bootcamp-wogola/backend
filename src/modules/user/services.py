from sqlalchemy import select
from .models import User, ProfessionalData
from src.core.security import get_password_hash
from src.core.exceptions import Conflict


# GET
async def get_user_by_id(db, user_id: int):
    return await db.get(User, user_id)


async def get_professional_by_id(db, user_id: int):
    return await db.get(ProfessionalData, user_id)


# POST
async def create_user(db, user):
    duplicate_user = await db.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if duplicate_user:
        return None

    user_data = user.model_dump(exclude={'password'})
    user_data['password'] = get_password_hash(user.password)

    new_user = User(**user_data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def create_professional_profile(db, user_id, professional_data):
    stmt = select(ProfessionalData).where(ProfessionalData.user_id == user_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        return Conflict('Professional profile already exists for this user')

    data_dict = professional_data.model_dump()
    data_dict['user_id'] = user_id

    new_profile = ProfessionalData(**data_dict)

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile


# PATCH
async def update_user(db, user_id: int, user_data):
    existing_user = await db.get(User, user_id)
    if not existing_user:
        return None

    updated_fields = user_data.model_dump(exclude_unset=True)

    if 'username' in updated_fields:
        conflicting_user = await db.scalar(
            select(User).where(
                (User.username == updated_fields['username'])
                & (User.id != user_id)
            )
        )
        if conflicting_user:
            raise ValueError('Username already exists.')

    if 'email' in updated_fields:
        conflicting_user = await db.scalar(
            select(User).where(
                (User.email == updated_fields['email']) & (User.id != user_id)
            )
        )
        if conflicting_user:
            raise ValueError('Email already exists.')

    for field, value in updated_fields.items():
        setattr(existing_user, field, value)

    await db.commit()
    await db.refresh(existing_user)

    return existing_user


async def update_professional_data(db, user_id, user_data):

    stmt = select(ProfessionalData).where(ProfessionalData.user_id == user_id)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        return None

    updated_fields = user_data.model_dump(exclude_unset=True)

    for field, value in updated_fields.items():
        setattr(existing_user, field, value)

    await db.commit()
    await db.refresh(existing_user)

    return existing_user


# DELETE
async def delete_user(db, user_id: int):
    existing_user = await db.get(User, user_id)
    if not existing_user:
        return None

    await db.delete(existing_user)
    await db.commit()

    return existing_user
