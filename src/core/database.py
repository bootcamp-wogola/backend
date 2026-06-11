from datetime import date
from typing import AsyncGenerator
from sqlalchemy import Date, func
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
    
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    updated_at: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(), 
        onupdate=func.current_date()
    )
