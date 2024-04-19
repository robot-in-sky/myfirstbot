"""Mocked Database."""
from sqlalchemy import MetaData

from app.db import Database, BaseModel


class MockedDatabase(Database):
    """Mocked database is used for integration tests."""

    async def teardown(self):
        """Clear all data in the database."""
        metadata: MetaData = BaseModel.metadata  # noqa
        for table in metadata.sorted_tables:
            await self.session.execute(table.delete())
        await self.session.commit()
