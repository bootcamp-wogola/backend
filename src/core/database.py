from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from .settings import get_settings

SETTINGS = get_settings()

ENGINE = create_async_engine(
    url=SETTINGS.DATABASE_URL,
    echo=SETTINGS.DEBUG,
)

ASYNC_SESSION = async_sessionmaker(
    ENGINE,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_SESSION() as session:
        yield session


class Base(DeclarativeBase):
    id : Mapped[int] = mapped_column(primary_key=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )
