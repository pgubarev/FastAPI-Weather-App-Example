__all__ = ('DB_ENGINE', 'db_session', 'setup_database', 'AsyncSession')

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    AsyncSession as BaseAsyncSession)
from sqlalchemy.orm import sessionmaker

from conf import settings

from .models.base import Base

DB_ENGINE = create_async_engine(settings.DATABASE_URL)

AsyncSession = sessionmaker(DB_ENGINE, expire_on_commit=False,
                            class_=BaseAsyncSession)


async def _on_application_startup():
    async with DB_ENGINE.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


def setup_database(app: FastAPI) -> None:
    app.add_event_handler('startup', _on_application_startup)


@asynccontextmanager
async def db_session() -> AsyncSession:
    async with AsyncSession() as session:
        async with session.begin():
            yield session
