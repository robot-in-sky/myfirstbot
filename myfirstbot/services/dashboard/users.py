from myfirstbot.base.entities.query import ChoiceQueryFilter, Pagination, Sorting
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.entities.choices.user_role import UserRole
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError
from myfirstbot.repo.pgsql.user import UserRepo


class DashboardUsersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.users = UserRepo(database)
        self.current_user = current_user


    async def get(self, id_: int) -> User:
        return await self.users.get(id_)


    async def get_all(
            self, role: UserRole | None = None, page: int = 1,
    ) -> list[User]:
        filters = []
        if role:
            filters.append(
                ChoiceQueryFilter(field="role", type="is", value=role),
            )
        return await self.users.get_many(
            filters=filters,
            pagination=Pagination(page=page, page_size=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    async def set_role(self, id_: int, role: UserRole) -> User | None:
        if self.current_user == UserRole.ADMINISTRATOR:
            return await self.users.set_role(id_, role)
        raise AccessDeniedError

