from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from src.entities.users.user import UserAdd

if TYPE_CHECKING:
    from src.deps import Dependencies


class CurrentUserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        deps: Dependencies = data["deps"]

        from_user = None
        chat_id = None
        if isinstance(event, Update):
            if event.message:
                from_user = event.message.from_user
                chat_id = event.message.chat.id
            if event.callback_query:
                from_user = event.callback_query.from_user

        if from_user:
            auth = deps.get_auth_service()
            user = UserAdd(telegram_id=from_user.id,
                           user_name=from_user.username or "",
                           first_name=from_user.first_name,
                           last_name=from_user.last_name,
                           chat_id=chat_id)
            data["current_user"] = await auth.synchronize_user(user)

        return await handler(event, data)
