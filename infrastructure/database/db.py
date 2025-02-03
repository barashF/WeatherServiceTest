from configuration.config import Config

from contextlib import asynccontextmanager, AbstractContextManager
from typing import AsyncIterator
from logging import Logger

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(Config.DB_URI, future=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
