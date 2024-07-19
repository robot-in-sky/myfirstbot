from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app.entities.user import UserAdd
from app.services.auth import AuthService

if TYPE_CHECKING:
    from app.repo.utils.database import Database


class CurrentUserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        db: Database = data["db"]

        from_user = None
        chat_id = None
        if isinstance(event, Update):
            if event.message:
                from_user = event.message.from_user
                chat_id = event.message.chat.id
            if event.callback_query:
                from_user = event.callback_query.from_user

        if from_user:
            data["current_user"] = await AuthService(db).synchronize_user(
                UserAdd(
                    telegram_id=from_user.id,
                    user_name=from_user.username or "",
                    first_name=from_user.first_name,
                    last_name=from_user.last_name,
                    chat_id=chat_id,
                )
            )

        return await handler(event, data)
