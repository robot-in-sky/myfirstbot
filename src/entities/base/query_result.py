from typing import Generic, TypeVar

from pydantic import BaseModel

from src.entities.base import Base as _EntityBase

_TQueryResultItem = TypeVar("_TQueryResultItem", bound=_EntityBase)
_TQueryCountBase = TypeVar("_TQueryCountBase")


class QueryResult(BaseModel, Generic[_TQueryResultItem]):
    items: list[_TQueryResultItem]
    page: int | None = None
    per_page: int | None = None
    total_pages: int | None = None
    total_items: int


class QueryCountItem(BaseModel, Generic[_TQueryCountBase]):
    value: _TQueryCountBase
    count: int
