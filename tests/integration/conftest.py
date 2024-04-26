import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.config import TestSettings
from tests.utils.mocked_database import Database


@pytest.fixture()
def settings() -> TestSettings:
    return TestSettings()


@pytest.fixture()
async def database(settings: TestSettings) -> Database:
    return Database(url=settings.db.url, echo=settings.debug)


@pytest_asyncio.fixture(scope="function")
async def session(database: Database) -> AsyncSession:
    async with database.make_session() as session:
        yield session
