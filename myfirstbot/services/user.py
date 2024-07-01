from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.query import Pagination, QueryResult, Sorting
from myfirstbot.entities.query.filters import ChoiceQueryFilter, QueryFilter
from myfirstbot.entities.user import User
from myfirstbot.exceptions import NotFoundError
from myfirstbot.repo import UserRepo
from myfirstbot.repo.utils.database import Database
from myfirstbot.services.utils.access_level import access_level


class UserService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.user_repo = UserRepo(database)
        self.current_user = current_user

    @access_level(required=UserRole.AGENT)
    async def get_all(
            self,
            role: UserRole | None = None,
            page: int = 1,
            per_page: int = 10,
    ) -> QueryResult[User]:
        filters: list[QueryFilter] = []
        if role:
            filters.append(
                ChoiceQueryFilter(field="role", type="is", value=role),
            )
        return await self.user_repo.get_all(
            filters=filters,
            pagination=Pagination(page=page, per_page=per_page),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.AGENT)
    async def get(self, id_: int) -> User:
        if user := await self.user_repo.get(id_):
            return user
        raise NotFoundError

    @access_level(required=UserRole.ADMINISTRATOR)
    async def set_role(self, id_: int, role: UserRole) -> int:
        if result := await self.user_repo.set_role(id_, role):
            return result
        raise NotFoundError
