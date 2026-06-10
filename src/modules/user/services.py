from sqlalchemy import select
from .model import User
from src.core.security import get_password_hash

#GET
async def get_user_by_id(db, user_id: int):
    user = await db.get(User, user_id)
    return user



# POST
async def create_user(db, user):
    duplicate_user = await db.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
        )
    )
    if duplicate_user:
        return None
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

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
                (User.email == updated_fields['email'])
                & (User.id != user_id)
            )
        )
        if conflicting_user:
            raise ValueError('Email already exists.')

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