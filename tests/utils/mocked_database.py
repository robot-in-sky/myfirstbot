from myfirstbot.base.repo.sql.database import Database
from myfirstbot.base.repo.sql.models.base import Base


class MockedDatabase(Database):

    async def clear(self) -> None:
        async with self.engine.connect() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                await connection.execute(table.delete())
                await connection.commit()
