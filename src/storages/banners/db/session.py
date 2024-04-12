from config.settings import settings

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio.engine import create_async_engine

async_engine = create_async_engine(settings.DB_URL, echo=True)
AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine, expire_on_commit=False
)
