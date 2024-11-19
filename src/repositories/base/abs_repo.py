from abc import abstractmethod
from typing import Generic, TypeVar

from src.entities.base import Base, QueryResult

_TEntity = TypeVar("_TEntity", bound=Base)
_TEntityAdd = TypeVar("_TEntityAdd", bound=Base)
_TEntityUpdate = TypeVar("_TEntityUpdate", bound=Base)
_TEntityQueryPaged = TypeVar("_TEntityQueryPaged", bound=Base)


class AbstractRepo(Generic[_TEntity, _TEntityAdd, _TEntityUpdate]):

    @abstractmethod
    async def add(self, instance: _TEntityAdd) -> _TEntity:
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
    async def get_many(self, query: _TEntityQueryPaged) -> QueryResult[_TEntity]:
        ...
