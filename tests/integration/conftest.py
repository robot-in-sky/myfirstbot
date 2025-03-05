import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import ENV_FILE_PATH
from src.infrastructure.database import DatabaseClient
from src.settings import AppSettings


@pytest.fixture(scope="module")
def settings() -> AppSettings:
    return AppSettings(_env_file=Path(ENV_FILE_PATH).parent.joinpath(".env.test"))


@pytest.fixture(scope="module")
def db(settings: AppSettings) -> DatabaseClient:
    return DatabaseClient(settings.db)


@pytest_asyncio.fixture(scope="function")
async def session(db: DatabaseClient) -> AsyncSession:
    await db.clear()
    async with db.get_session() as session:
        yield session


@pytest.fixture(scope="module")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()
