from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

TSchema = TypeVar("TSchema")


class AbstractRepo(Generic[TSchema]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def add(self, **attrs: Any) -> TSchema:
        ...

    @abstractmethod
    async def get(self, ident: int) -> TSchema | None:
        ...

    @abstractmethod
    async def update(self, ident: int, **attrs: Any) -> TSchema | None:
        ...

    @abstractmethod
    async def delete(self, ident: int) -> None:
        ...
