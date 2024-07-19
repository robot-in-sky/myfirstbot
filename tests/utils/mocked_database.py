from app.repo.models import OrmBase
from app.repo.utils import Database


class MockedDatabase(Database):

    async def clear(self) -> None:
        async with self.engine.connect() as connection:
            for table in reversed(OrmBase.metadata.sorted_tables):
                await connection.execute(table.delete())
                await connection.commit()
