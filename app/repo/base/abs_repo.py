from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from app.entities.base import Base
from app.entities.query import Pagination, QueryFilter, QueryResult, Sorting

_TEntity = TypeVar("_TEntity", bound=Base)
_TEntityCreate = TypeVar("_TEntityCreate", bound=Base)
_TEntityUpdate = TypeVar("_TEntityUpdate", bound=Base)


class AbstractRepo(Generic[_TEntity, _TEntityCreate, _TEntityUpdate]):

    @abstractmethod
    async def add(self, instance: _TEntityCreate) -> _TEntity:
        ...

    @abstractmethod
    async def get(self, id_: int) -> _TEntity | None:
        ...

    @abstractmethod
    async def update(self, id_: int, instance: _TEntityUpdate) -> _TEntity | None:
        ...

    @abstractmethod
    async def delete(self, id_: int) -> int | None:
        ...

    @abstractmethod
    async def get_all(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> QueryResult[_TEntity]:
        ...
