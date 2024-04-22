"""Database middleware is a common way to inject database dependency in handlers."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.db.database import Database
from myfirstbot.tgbot.structures.data_structure import TransferData


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        """This method calls each update of Message or CallbackQuery type."""
        async with AsyncSession(bind=data["engine"]) as session:
            data["db"] = Database(session)
            return await handler(event, data)
