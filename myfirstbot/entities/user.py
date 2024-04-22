from myfirstbot.base.entities.base import Base
from myfirstbot.entities.enums.access_level import AccessLevel


class UserCreate(Base):
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel | None = None


class User(Base):
    id: int
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel


class UserUpdate(Base):
    user_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel | None = None
