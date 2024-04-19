"""Mocked Database."""
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL

from app.config import settings
from app.db import Database, BaseModel
from app.db.db import create_async_engine


DEFAULT_DB_URL = settings.db.url_test


def mocked_async_engine(url: URL | str = DEFAULT_DB_URL):
    """Mocked engine is used for integration tests."""
    return create_async_engine(url)


class MockedDatabase(Database):
    """Mocked database is used for integration tests."""

    async def teardown(self):
        """Clear all data in the database."""
        metadata: MetaData = BaseModel.metadata  # noqa
        for table in metadata.sorted_tables:
            await self.session.execute(table.delete())
        await self.session.commit()

