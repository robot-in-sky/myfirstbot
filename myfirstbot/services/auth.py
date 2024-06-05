
from myfirstbot.config import settings
from myfirstbot.entities.choices.user_role import UserRole
from myfirstbot.entities.user import User, UserAdd, UserUpdate
from myfirstbot.repo import UserRepo
from myfirstbot.repo.utils import Database


class AuthService:

    def __init__(self, database: Database) -> None:
        self.user_repo = UserRepo(database)


    async def synchronize_user(self, data: UserAdd) -> User:
        if user := await self.user_repo.get_by_telegram_id(data.telegram_id):
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
                ))
        else:
            user = await self.user_repo.add(data)

        if (settings.default_admins
                and user.telegram_id in settings.default_admins
                and user.role != UserRole.ADMINISTRATOR):
            await self.user_repo.set_role(user.id, UserRole.ADMINISTRATOR)
            user = await self.user_repo.get(user.id)

        return user
