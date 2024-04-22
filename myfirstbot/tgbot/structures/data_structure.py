"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from myfirstbot.db.database import Database
from myfirstbot.entities.user import User


class TransferData(TypedDict):
    """Common transfer data."""

    engine: AsyncEngine
    db: Database
    bot: Bot
    user: User
