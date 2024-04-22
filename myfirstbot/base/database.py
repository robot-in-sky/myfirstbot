from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine as _create_async_engine

from myfirstbot.config import settings

# from myfirstbot.db.order import OrderRepo
# from myfirstbot.db.user import UserRepo


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(
        url=url,
        echo=settings.debug,
        pool_pre_ping=True,
    )


class Database:

    engine: AsyncEngine
    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        # self.user = UserRepo(session=session)
        # self.order = OrderRepo(session=session)

