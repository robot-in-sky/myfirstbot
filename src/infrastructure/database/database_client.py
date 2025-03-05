from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .database_settings import DatabaseSettings


class DatabaseClient:

    def __init__(self, settings: DatabaseSettings) -> None:
        self.engine = create_async_engine(
            url=settings.url, echo=settings.echo,
        )
        self.get_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession,
        )

    async def add_uuid_extension(self) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))

    async def create_tables_by_base(self, sqlalchemy_base: type[DeclarativeBase]) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(sqlalchemy_base.metadata.create_all)

    async def drop_tables_by_base(self, sqlalchemy_base: type[DeclarativeBase]) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(sqlalchemy_base.metadata.drop_all)
