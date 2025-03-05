import logging

from src.entities.users import User, UserAdd, UserUpdate
from src.infrastructure.database import DatabaseClient
from src.repositories import UserRepo


class AuthService:

    def __init__(self, db: DatabaseClient) -> None:
        self._user_repo = UserRepo(db)


    async def synchronize_user(self, data: UserAdd) -> User:
        user = await self._user_repo.get_by_telegram_id(data.telegram_id)
        if user is None:
            user = await self._user_repo.add(data)
            logging.info(f"New user: @{user.user_name}")

        elif (data.user_name != user.user_name or
                data.first_name != user.user_name or
                    data.last_name != user.last_name or
                        data.chat_id and data.chat_id != user.chat_id):

            user = await self._user_repo.update(
                                user.id, UserUpdate(user_name=data.user_name,
                                                    first_name=data.first_name,
                                                    last_name=data.last_name,
                                                    chat_id=data.chat_id)) or user
            logging.info(f"User updated: @{user.user_name}")

        """
        if (settings.default_admins and
                user.telegram_id in deps.settings.default_admins and
                                user.role != UserRole.ADMINISTRATOR):

            await self.user_repo.set_role(user.id, UserRole.ADMINISTRATOR)
            user = await self.user_repo.get(user.id) or user
        """

        return user
