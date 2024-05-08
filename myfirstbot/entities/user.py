from datetime import UTC, datetime

from myfirstbot.base.entities.base import Base
from myfirstbot.entities.choices.access_level import AccessLevel


class UserCreate(Base):
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel | None = AccessLevel.USER
    created: datetime = datetime.now(UTC)
    updated: datetime = datetime.now(UTC)


class User(Base):
    id: int
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel
    created: datetime
    updated: datetime


class UserUpdate(Base):
    user_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel | None = None
    updated: datetime = datetime.now(UTC)
