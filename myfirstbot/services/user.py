from myfirstbot.base.database import Database
from myfirstbot.entities.enums.access_level import AccessLevel
from myfirstbot.entities.user import User, UserCreate, UserUpdate
from myfirstbot.repositories import UserRepo


class UserService:
    def __init__(self, database: Database) -> None:
        session = database.make_session()
        self.repo = UserRepo(session)

    async def add(
        self,
        telegram_id: int,
        user_name: str,
        first_name: str | None = None,
        last_name: str | None = None,
        chat_id: int | None = None,
        access_level: AccessLevel | None = AccessLevel.USER
    ) -> User:
        return self.repo.add(UserCreate(
            telegram_id=telegram_id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id,
            access_level=access_level
        ))

    async def get(self, id_: int) -> User | None:
        return self.repo.get(id_)

    async def delete(self, id_: int) -> None:
        return self.repo.delete(id_)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.repo.get_by_telegram_id(telegram_id)

    async def get_all(
            self, access_level: AccessLevel | None = None, *,
            skip: int = 0, limit: int = -1, order_by: str | None = None
    ) -> list[User]:
        return self.repo.get_all(
            access_level=access_level,
            skip=skip,
            limit=limit,
            order_by=order_by
        )

    async def update_telegram_info(  # noqa: PLR0913
        self, id_: int,
        user_name: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        chat_id: int | None = None,
    ) -> User | None:
        return await self.repo.update(id_, UserUpdate(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id
        ))

    async def set_access_level(
            self, id_: int, access_level: AccessLevel,
    ) -> User:
        return await self.repo.update(
            id_, UserUpdate(access_level=access_level)
        )