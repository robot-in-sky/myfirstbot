from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from myfirstbot.config import DatabaseSettings


class Database:

    def __init__(self, settings: DatabaseSettings) -> None:
        self.engine = create_async_engine(
            url=settings.url, echo=settings.echo,
        )
        self.get_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession,
        )
