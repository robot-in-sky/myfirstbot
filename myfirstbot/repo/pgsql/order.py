from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.query import FilterGroup, Pagination, QueryFilter, Sorting
from myfirstbot.base.repo.sql.abs_repo import AbstractRepo
from myfirstbot.base.repo.sql.exc_mapper import exception_mapper
from myfirstbot.base.repo.sql.query_utils import apply_filter, apply_filters, apply_pagination, apply_sorting
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repo.pgsql.models.order import Order as _OrderOrm


class OrderRepo(AbstractRepo[Order, OrderCreate, OrderUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @exception_mapper
    async def add(self, instance: OrderCreate) -> Order:
        query = (insert(_OrderOrm).values(**instance.model_dump())
                 .returning(_OrderOrm))
        result = await self.session.scalar(query)
        await self.session.commit()
        return Order.model_validate(result)

    async def get(self, id_: int) -> Order | None:
        query = select(_OrderOrm).where(_OrderOrm.id == id_)
        result = await self.session.scalar(query)
        return Order.model_validate(result) if result else None

    async def get_many(
            self,
            filters: Sequence[QueryFilter] | FilterGroup | None = None,
            *,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> list[Order]:
        query = select(_OrderOrm)
        if filters:
            query = apply_filters(query, filters)
        if sorting:
            query = apply_sorting(query, sorting)
        if pagination:
            query = apply_pagination(query, pagination)
        result = (await self.session.scalars(query)).all()
        return list(map(Order.model_validate, result))

    @exception_mapper
    async def update(self, id_: int, instance: OrderUpdate) -> Order:
        values = instance.model_dump()
        query = (update(_OrderOrm).where(_OrderOrm.id == id_)
                 .values(**values).returning(_OrderOrm))
        result = await self.session.scalar(query)
        await self.session.commit()
        return Order.model_validate(result)

    @exception_mapper
    async def delete(self, id_: int) -> None:
        query = delete(_OrderOrm).where(_OrderOrm.id == id_)
        await self.session.execute(query)
        await self.session.commit()

    async def get_one(self, filter_: QueryFilter) -> Order | None:
        query = apply_filter(select(_OrderOrm), filter_)
        result = await self.session.scalar(query)
        return Order.model_validate(result) if result else None
