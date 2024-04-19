"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.db import Database
from app.db.schemas.user import UserSchema


class TransferData(TypedDict):
    """Common transfer data."""

    engine: AsyncEngine
    db: Database
    bot: Bot
    user: UserSchema
