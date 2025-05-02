from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from core.entities.users.user import UserAdd

if TYPE_CHECKING:
    from interfaces.tgbot.tgbot_deps import TgBotDependencies


class CurrentUserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        deps: TgBotDependencies = data["deps"]
        if tg_user := data.get("event_from_user"):
            auth = deps.get_auth_service()
            user = UserAdd(telegram_id=tg_user.id,
                           user_name=tg_user.username,
                           first_name=tg_user.first_name,
                           last_name=tg_user.last_name,
                           active=True)
            data["current_user"] = await auth.synchronize_user(user)

        return await handler(event, data)
