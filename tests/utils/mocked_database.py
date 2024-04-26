from myfirstbot.base.database import Database
from myfirstbot.base.repositories.sql.models.base import Base


class MockedDatabase(Database):

    async def teardown(self) -> None:
        """Clear all data in the database."""
        for table in Base.metadata.sorted_tables:
            await self.session.execute(table.delete())
        await self.session.commit()

