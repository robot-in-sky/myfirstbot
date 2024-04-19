from typing import Any, TypeVar
from collections.abc import Sequence

from app.db.repositories.abs_repo import AbstractRepo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


TModel = TypeVar('TModel')


class AbstractOrmRepo(AbstractRepo[TModel]):

    def __init__(self, session: AsyncSession, model: TModel):
        super().__init__(session)
        self.model = model

    async def add(self, **attrs: Any) -> TModel:
        instance = self.model(**attrs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, ident: int) -> TModel | None:
        return await self.session.get(self.model, ident)

    async def get_one(self, **filter_by: Any) -> TModel | None:
        statement = select(self.model).filter_by(**filter_by)
        return await self.session.scalar(statement)

    async def get_many(
        self, skip: int = 0, limit: int = 100, order_by=None, **filter_by
    ) -> Sequence[TModel]:
        statement = select(self.model).filter_by(**filter_by)
        statement = statement.offset(skip).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)
        return (await self.session.scalars(statement)).all()

    async def update(self, ident: int, **attrs: Any) -> TModel:
        if instance := await self.session.get(self.model, ident):
            for k, v in attrs.items():
                setattr(instance, k, v)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance

    async def delete(self, ident: int) -> None:
        if instance := self.session.get(self.model, ident):
            await self.session.delete(instance)
            await self.session.commit()
