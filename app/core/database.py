from typing import Any, AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.models import Base

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{settings.db_user}:{settings.db_password}'
    f'@{settings.db_host}/{settings.db_name}'
)


engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        yield session


session_dep = Annotated[AsyncSession, Depends(get_session)]
