import logging
from uuid import UUID

from clients.database import DatabaseClient
from core.entities.base import QueryCountItem, QueryResult
from core.entities.users import User, UserQuery, UserQueryPaged, UserRole
from core.exceptions import NotFoundError
from core.repositories import UserRepo
from core.services.utils.access_level import access_level


class UserManageService:
    def __init__(self, db: DatabaseClient, current_user: User) -> None:
        self._user_repo = UserRepo(db)
        self.current_user = current_user


    # @access_level(required=UserRole.AGENT)
    async def get_user(self, id_: UUID) -> User:
        if user := await self._user_repo.get(id_):
            return user
        raise NotFoundError


    # @access_level(required=UserRole.ADMINISTRATOR)
    async def set_user_role(self, id_: UUID, role: UserRole) -> UUID:
        if user_id := await self._user_repo.set_role(id_, role):
            logging.info(f"User #{user_id}: role updated to {role.name} by @{self.current_user.user_name}")
            return user_id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def get_users(self, query: UserQueryPaged) -> QueryResult[User]:
        return await self._user_repo.get_many(query)


    @access_level(required=UserRole.AGENT)
    async def get_user_count(self, query: UserQuery) -> int:
        return await self._user_repo.get_count(query)


    @access_level(required=UserRole.AGENT)
    async def get_user_count_by_role(self, query: UserQuery) -> list[QueryCountItem[UserRole]]:
        return await self._user_repo.get_count_by_role(query)
