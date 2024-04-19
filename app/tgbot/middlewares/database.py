"""Database middleware is a common way to inject database dependency in handlers."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.tgbot.structures.data_structure import TransferData
from app.db.db import Database


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls each update of Message or CallbackQuery type."""
        new_session = async_sessionmaker(data['engine'], expire_on_commit=False)
        # async with AsyncSession(bind=data['engine']) as session:
        async with new_session() as session:
            data['db'] = Database(session)
            return await handler(event, data)
