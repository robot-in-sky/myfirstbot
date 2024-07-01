from collections.abc import Sequence
from datetime import UTC, datetime
from math import ceil

from pydantic import TypeAdapter
from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.query import CountedResultItem, Pagination, QueryFilter, QueryResult, Sorting
from myfirstbot.repo.base import AbstractRepo
from myfirstbot.repo.models import Order as _OrderOrm
from myfirstbot.repo.utils import Database, exception_mapper
from myfirstbot.repo.utils.query_utils import apply_filters, apply_pagination, apply_sorting, get_count


class OrderRepo(AbstractRepo[Order, OrderAdd, OrderUpdate]):

    def __init__(self, database: Database) -> None:
        self.db = database

    @exception_mapper
    async def add(self, instance: OrderAdd) -> Order:
        query = (insert(_OrderOrm).values(**instance.model_dump())
                 .returning(_OrderOrm))
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            await session.commit()
            return Order.model_validate(result)

    async def get(self, id_: int) -> Order | None:
        query = select(_OrderOrm).where(_OrderOrm.id == id_)
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                return Order.model_validate(result)
            return None

    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        query = (update(_OrderOrm).where(_OrderOrm.id == id_)
                 .values(**instance.model_dump(), updated=datetime.now(UTC))
                 .returning(_OrderOrm))
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return Order.model_validate(result)
            return None

    async def delete(self, id_: int) -> int | None:
        query = delete(_OrderOrm).where(_OrderOrm.id == id_).returning(_OrderOrm.id)
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return result
            return None

    async def set_status(self, id_: int, status: OrderStatus) -> int | None:
        query = (update(_OrderOrm).where(_OrderOrm.id == id_)
                 .values(status=status, updated=datetime.now(UTC))
                 .returning(_OrderOrm.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return result
            return None

    async def get_all(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> QueryResult[Order]:
        query = select(_OrderOrm)
        if filters:
            query = apply_filters(query, filters, or_=or_)

        async with self.db.get_session() as session:
            total_items = await get_count(session, query)

            if sorting:
                query = apply_sorting(query, sorting)

            page, per_page, total_pages = None, None, None

            if pagination and total_items > 0:
                query = apply_pagination(query, pagination)
                page = pagination.page
                per_page = pagination.per_page
                total_pages = ceil(total_items / pagination.per_page)

            orm_items = (await session.scalars(query)).all()
            items = TypeAdapter(list[Order]).validate_python(orm_items)

            return QueryResult[Order](
                items=items,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                total_items=total_items,
            )

    async def get_count(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
    ) -> int:
        query = select(_OrderOrm)
        if filters:
            query = apply_filters(query, filters, or_=or_)

        async with self.db.get_session() as session:
            return await get_count(session, query)

    async def get_count_by_status(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
    ) -> list[CountedResultItem[OrderStatus]]:
        column = _OrderOrm.status
        query = select(column, func.count(column))
        if filters:
            query = apply_filters(query, filters, or_=or_)
        query = query.group_by(column).order_by(column)

        async with self.db.get_session() as session:
            result = (await session.execute(query)).all()
            return [CountedResultItem[OrderStatus](
                value=item[0], count=item[1],
            ) for item in result]
