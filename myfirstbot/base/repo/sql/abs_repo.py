from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.base import Base as _EntityBase
from myfirstbot.base.entities.query import FilterGroup, Pagination, QueryFilter, Sorting

_TEntity = TypeVar("_TEntity", bound=_EntityBase)
_TEntityCreate = TypeVar("_TEntityCreate", bound=_EntityBase)
_TEntityUpdate = TypeVar("_TEntityUpdate", bound=_EntityBase)


class AbstractRepo(Generic[_TEntity, _TEntityCreate, _TEntityUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def add(self, instance: _TEntityCreate) -> _TEntity:
        ...

    @abstractmethod
    async def get(self, id_: int) -> _TEntity | None:
        ...

    @abstractmethod
    async def get_many(
            self,
            filters: Sequence[QueryFilter] | FilterGroup | None = None,
            *,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> list[_TEntity]:
        ...

    @abstractmethod
    async def update(self, id_: int, instance: _TEntityUpdate) -> _TEntity:
        ...

    @abstractmethod
    async def delete(self, id_: int) -> None:
        ...
