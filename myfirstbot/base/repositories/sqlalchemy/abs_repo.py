from abc import abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.base import Base as _EntityBase

TEntity = TypeVar("TEntity", bound=_EntityBase)
TEntityCreate = TypeVar("TEntityCreate", bound=_EntityBase)
TEntityUpdate = TypeVar("TEntityUpdate", bound=_EntityBase)


class AbstractRepo(Generic[TEntity, TEntityCreate, TEntityUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def add(self, instance: TEntityCreate) -> TEntity:
        ...

    @abstractmethod
    async def get(self, id_: int) -> TEntity | None:
        ...

    @abstractmethod
    async def update(self, id_: int, instance: TEntityUpdate) -> TEntity:
        ...

    @abstractmethod
    async def delete(self, id_: int) -> None:
        ...
