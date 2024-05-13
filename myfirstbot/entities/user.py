from datetime import datetime

from myfirstbot.base.entities.base import Base
from myfirstbot.entities.choices.user_role import UserRole


class UserAdd(Base):
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None


class User(Base):
    id: int
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    role: UserRole
    created: datetime
    updated: datetime


class UserUpdate(Base):
    user_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
