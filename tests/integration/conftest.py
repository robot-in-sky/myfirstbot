import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.config import Settings
from myfirstbot.definitions import ENVFILE_PATH
from tests.utils.mocked_database import MockedDatabase


@pytest.fixture(scope="module")
def settings() -> Settings:
    return Settings(_env_file=Path(ENVFILE_PATH).parent.joinpath(".env.test"))


@pytest.fixture(scope="module")
def database(settings: Settings) -> MockedDatabase:
    return MockedDatabase(settings.db)


@pytest_asyncio.fixture(scope="function")
async def session(database: MockedDatabase) -> AsyncSession:
    await database.clear()
    async with database.get_session() as session:
        yield session


@pytest.fixture(scope="module")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()
