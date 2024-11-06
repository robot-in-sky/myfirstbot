import logging

from src.config import settings
from src.entities.choices.user_role import UserRole
from src.entities.user import User, UserAdd, UserUpdate
from src.repositories import UserRepo
from src.repositories.utils import Database


class AuthService:

    def __init__(self, database: Database) -> None:
        self.user_repo = UserRepo(database)


    async def synchronize_user(self, data: UserAdd) -> User:
        user = await self.user_repo.get_by_telegram_id(data.telegram_id)
        if user is not None:
            if (
                (data.user_name,
                 data.first_name,
                 data.last_name) !=

                (user.user_name,
                 user.first_name,
                 user.last_name) or

                (data.chat_id and data.chat_id != user.chat_id)
            ):
                user = await self.user_repo.update(user.id, UserUpdate(
                    user_name=data.user_name,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    chat_id=data.chat_id,
                )) or user
                logging.info(f"User updated: @{user.user_name}")
        else:
            user = await self.user_repo.add(data)
            logging.info(f"New user: @{user.user_name}")

        """
        if (settings.default_admins
                and user.telegram_id in settings.default_admins
                and user.role != UserRole.ADMINISTRATOR):
            await self.user_repo.set_role(user.id, UserRole.ADMINISTRATOR)
            user = await self.user_repo.get(user.id) or user
        """

        return user
