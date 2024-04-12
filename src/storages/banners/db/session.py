from asyncio import current_task

from config.settings import settings
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio.engine import create_async_engine

async_engine = create_async_engine(settings.DB_URL, echo=False)
AsyncSessionFactory: async_sessionmaker = async_sessionmaker(
    bind=async_engine, expire_on_commit=False
)
DatabaseConnection = async_scoped_session(
    session_factory=AsyncSessionFactory, scopefunc=current_task
)
