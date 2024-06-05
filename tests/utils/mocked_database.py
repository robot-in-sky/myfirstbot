from myfirstbot.repo.models import Base
from myfirstbot.repo.utils import Database


class MockedDatabase(Database):

    async def clear(self) -> None:
        async with self.engine.connect() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                await connection.execute(table.delete())
                await connection.commit()
