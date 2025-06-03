from datetime import datetime
from typing import Literal
from uuid import UUID

from core.entities.base import Base

from .enums.user_role import UserRole


class UserAdd(Base):
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    active: bool = True


class User(Base):
    id: UUID
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserUpdate(Base):
    user_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    active: bool = True


class UserQuery(Base):
    role: UserRole | None = None
    role__in: set[UserRole] | None = None
    search: str | None = None


class UserQueryPaged(UserQuery):
    sort_by: str | None = "created_at"
    sort: Literal["asc", "desc"] | None = "desc"
    page: int = 1
    per_page: int = 10


USER_SEARCH_BY = [
    "user_name",
    "first_name",
    "last_name",
]


__all__ = [
    "UserAdd",
    "User",
    "UserUpdate",
    "UserQuery",
    "UserQueryPaged",
    "USER_SEARCH_BY",
]
