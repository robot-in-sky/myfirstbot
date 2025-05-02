import logging

from clients.database import DatabaseClient
from core.entities.users import User, UserAdd, UserUpdate
from core.repositories import UserRepo


class AuthService:

    def __init__(self, db: DatabaseClient) -> None:
        self._user_repo = UserRepo(db)


    async def synchronize_user(self, data: UserAdd) -> User:

        user = await self._user_repo.get_by_telegram_id(data.telegram_id)

        if user is None:
            user = await self._user_repo.add(data)
            logging.info(f"New user: @{user.user_name}")

        elif ((data.user_name, data.first_name, data.last_name, data.active) !=
                        (user.user_name, user.first_name, user.last_name, user.active)):

            user = await self._user_repo.update(
                                user.id, UserUpdate(user_name=data.user_name,
                                                    first_name=data.first_name,
                                                    last_name=data.last_name,
                                                    active=data.active)) or user

            logging.info(f"User updated: @{user.user_name}\n")

        """
        if (settings.default_admins and
                user.telegram_id in deps.settings.default_admins and
                                user.role != UserRole.ADMINISTRATOR):

            await self.user_repo.set_role(user.id, UserRole.ADMINISTRATOR)
            user = await self.user_repo.get(user.id) or user
        """

        return user
