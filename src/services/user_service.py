import logging

from src.entities.base import QueryCountItem, QueryResult
from src.entities.choices import UserRole
from src.entities.user import User, UserQuery, UserQueryPaged
from src.exceptions import AccessDeniedError, NotFoundError
from src.io.database import DatabaseClient
from src.repositories import UserRepo
from src.services.utils.access_level import access_level


class UserService:

    def __init__(self, database: DatabaseClient, current_user: User) -> None:
        self.user_repo = UserRepo(database)
        self.current_user = current_user


    @access_level(required=UserRole.USER)
    async def get(self, id_: int) -> User:
        if self.current_user.role < UserRole.AGENT and id_ != self.current_user.id:
            raise AccessDeniedError
        if user := await self.user_repo.get(id_):
            return user
        raise NotFoundError


    @access_level(required=UserRole.USER) # ADMINISTRATOR
    async def set_role(self, id_: int, role: UserRole) -> int:
        if self.current_user.role < UserRole.AGENT and id_ != self.current_user.id:
            raise AccessDeniedError
        if user_id := await self.user_repo.set_role(id_, role):
            logging.info(f"User #{user_id}: role updated to {role.name} by @{self.current_user.user_name}")
            return user_id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def get_many(self, query: UserQueryPaged) -> QueryResult[User]:
        return await self.user_repo.get_many(query)


    @access_level(required=UserRole.AGENT)
    async def get_count(self, query: UserQuery) -> int:
        return await self.user_repo.get_count(query)


    @access_level(required=UserRole.AGENT)
    async def get_count_by_role(self, query: UserQuery) -> list[QueryCountItem[UserRole]]:
        return await self.user_repo.get_count_by_role(query)
