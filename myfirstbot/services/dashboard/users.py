from myfirstbot.base.entities.query import ChoiceQueryFilter, Pagination, Sorting
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.base.services.access_level import access_level
from myfirstbot.entities.choices.user_role import UserRole
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, NotFoundError
from myfirstbot.repo.pgsql.user import UserRepo


class DashboardUsersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.user_repo = UserRepo(database)
        self.current_user = current_user


    @access_level(required=UserRole.AGENT)
    async def get(self, id_: int) -> User:
        if user := await self.user_repo.get(id_):
            return user
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def get_all(
            self, role: UserRole | None = None, page: int = 1,
    ) -> list[User]:
        filters = []
        if role:
            filters.append(
                ChoiceQueryFilter(field="role", type="is", value=role),
            )
        return await self.user_repo.get_many(
            filters=filters,
            pagination=Pagination(page=page, page_size=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.ADMINISTRATOR)
    async def set_role(self, id_: int, role: UserRole) -> int:
        if result := await self.user_repo.set_role(id_, role):
            return result
        raise NotFoundError
