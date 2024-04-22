from pathlib import Path

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from myfirstbot.base.database import create_async_engine
from myfirstbot.definitions import ENVFILE_PATH
from myfirstbot.tgbot.dispatcher import get_dispatcher
from tests.utils.config import TestSettings
from tests.utils.mocked_bot import MockedBot
from tests.utils.mocked_database import MockedDatabase

TEST_ENVFILE_PATH = Path(ENVFILE_PATH).parent.joinpath(".env.test")


@pytest.fixture()
def settings() -> TestSettings:
    return TestSettings(_env_file=TEST_ENVFILE_PATH)


@pytest.fixture()
def engine(settings: TestSettings) -> AsyncEngine:
    return create_async_engine(settings.db.url)


@pytest_asyncio.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncSession:
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def db(session: AsyncSession) -> MockedDatabase:
    database = MockedDatabase(session)
    await database.teardown()
    return database


@pytest.fixture()
def bot() -> MockedBot:
    return MockedBot()


@pytest.fixture()
def storage() -> MemoryStorage:
    return MemoryStorage()


@pytest.fixture()
def dp(storage: BaseStorage) -> Dispatcher:
    return get_dispatcher(storage=storage)

