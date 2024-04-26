from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Database:

    def __init__(
        self, url: URL | str, *, echo: bool = False,
    ) -> None:
        self.engine = create_async_engine(
            url, echo=echo, pool_pre_ping=True,
        )
        self.make_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession,
        )
