from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from core.entities.base import Base
from core.entities.users import User

from .enums.app_form_status import AppFormStatus
from .visa import Country, Visa


class AppFormAdd(Base):
    user_id: UUID
    country: Country
    visa_id: str
    data: dict[str, Any] | None = None


class AppForm(Base):
    id: UUID
    user_id: UUID
    user: User
    country: Country
    visa_id: str
    visa: Visa | None = None
    data: dict[str, Any] | None = None
    given_name: str | None = None
    surname: str | None = None
    status: AppFormStatus
    created_at: datetime
    updated_at: datetime


class AppFormUpdate(Base):
    data: dict[str, Any] | None = None


class AppFormQuery(Base):
    user_id: UUID | None = None
    country: Country | None = None
    country__in: set[Country] | None = None
    status: AppFormStatus | None = None
    status__in: set[AppFormStatus] | None = None
    status__not_in: set[AppFormStatus] | None = None


class AppFormQueryPaged(AppFormQuery):
    sort_by: str | None = "created_at"
    sort: Literal["asc", "desc"] | None = "desc"
    page: int = 1
    per_page: int = 10


__all__ = [
    "AppFormAdd",
    "AppForm",
    "AppFormUpdate",
    "AppFormQuery",
    "AppFormQueryPaged",
]
