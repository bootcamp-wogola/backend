from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.models import User, UserRole
from .database import get_db
from .settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')
password_hasher = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


async def authenticate_user_service(
    *, session: AsyncSession, email: str, password: str
) -> User | None:
    user = await session.scalar(
        select(User).where(User.email == email)
    )
    if not user:
        return None

    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict) -> str:
    token_payload = data.copy()
    token_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


async def get_current_user(
    session: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    invalid_token_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iat': True,
            },
        )

        token_email = decoded_token.get('sub')
        if not token_email:
            raise invalid_token_exception

        user = await session.scalar(
            select(User).where(User.email == token_email)
        )
        if not user:
            raise invalid_token_exception

        return user

    except JWTError:
        raise invalid_token_exception


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to access this resource.',
        )
    return current_user