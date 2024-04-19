from abc import abstractmethod
from typing import Any, Generic, TypeVar
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

TSchema = TypeVar('TSchema')


class AbstractRepo(Generic[TSchema]):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def add(self, **attrs: Any) -> TSchema:
        ...

    @abstractmethod
    async def get(self, ident: int) -> TSchema | None:
        ...

    @abstractmethod
    async def get_one(self, **filter_by: Any) -> TSchema | None:
        ...

    @abstractmethod
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by=None, **filter_by
    ) -> Sequence[TSchema]:
        ...

    @abstractmethod
    async def update(self, ident: int, **attrs: Any) -> TSchema | None:
        ...

    @abstractmethod
    async def delete(self, ident: int) -> None:
        ...
