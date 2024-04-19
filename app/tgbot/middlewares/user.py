"""Role middleware used for get role of user for followed filtering."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.tgbot.structures.data_structure import TransferData
from app.db import Database


class UserMiddleware(BaseMiddleware):
    """This class is used for getting user role from database."""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData,
    ) -> Any:
        """This method calls each update of Message or CallbackQuery type."""
        db: Database = data['db']

        user = await db.user.get_one_by_telegram_id(event.from_user.id)
        if not user:
            user = await db.user.new(
                telegram_id=event.from_user.id,
                user_name=event.from_user.username,
                chat_id=event.chat.id
            )
        else:
            if user.user_name != event.from_user.user_name or \
                    user.first_name != event.from_user.first_name or \
                    user.last_name != event.from_user.last_name or \
                    user.chat_id != event.chat.id:
                db.user.update(
                    user_name=event.from_user.user_name,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name,
                    chat_id=event.chat.id
                )

        data['user'] = user
        return await handler(event, data)
