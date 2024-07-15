from typing import Generic, TypeVar

from pydantic import BaseModel

from myfirstbot.entities.base import Base as _EntityBase

_TResultItem = TypeVar("_TResultItem", bound=_EntityBase)
_TCountResultBase = TypeVar("_TCountResultBase")


class QueryResult(BaseModel, Generic[_TResultItem]):
    items: list[_TResultItem]
    page: int | None = None
    per_page: int | None = None
    total_pages: int | None = None
    total_items: int


class CountResultItem(BaseModel, Generic[_TCountResultBase]):
    value: _TCountResultBase
    count: int
