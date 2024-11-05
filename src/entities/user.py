from datetime import datetime
from typing import Literal

from pydantic import PositiveInt

from src.entities.base import Base
from src.entities.choices import UserRole


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


class UserQuery(Base):
    role: UserRole | None = None
    role__in: set[UserRole] | None = None
    search: str | None = None


class UserQueryPaged(UserQuery):
    sort_by: str | None = None
    sort: Literal["asc", "desc"] = "asc"
    page: int = 1
    per_page: int = 10
