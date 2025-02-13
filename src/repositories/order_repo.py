from datetime import datetime
from math import ceil

from pydantic import TypeAdapter
from pytz import UTC
from sqlalchemy import Select, and_, delete, func, select, update
from sqlalchemy.dialects.postgresql import insert

from src.entities.base import QueryCountItem, QueryResult
from src.entities.order import (
    Order,
    OrderAdd,
    OrderQuery,
    OrderQueryPaged,
    OrderSearchBy,
    OrderStatus,
    OrderUpdate,
)
from src.io.database import DatabaseClient
from src.repositories.base import AbstractRepo
from src.repositories.orm_models import OrmOrder
from src.repositories.utils import exception_mapper
from src.repositories.utils.query_utils import (
    apply_pagination,
    apply_search,
    apply_sorting,
    get_column,
    get_row_count,
    match_types,
)


class OrderRepo(AbstractRepo[Order, OrderAdd, OrderUpdate]):

    def __init__(self, db: DatabaseClient) -> None:
        self.db = db


    @exception_mapper
    async def add(self, instance: OrderAdd) -> Order:
        stmt = (insert(OrmOrder).values(**instance.model_dump())
                 .returning(OrmOrder))
        async with self.db.get_session() as session:
            result = await session.scalar(stmt)
            await session.commit()
            return Order.model_validate(result)


    async def get(self, id_: int) -> Order | None:
        stmt = select(OrmOrder).where(OrmOrder.id == id_)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                return Order.model_validate(result)
            return None


    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        stmt = (update(OrmOrder).where(OrmOrder.id == id_)
                 .values(**instance.model_dump(), updated_at=datetime.now(UTC))
                 .returning(OrmOrder))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return Order.model_validate(result)
            return None


    async def delete(self, id_: int) -> int | None:
        stmt = delete(OrmOrder).where(OrmOrder.id == id_).returning(OrmOrder.id)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None


    async def set_status(self, id_: int, status: OrderStatus) -> int | None:
        stmt = (update(OrmOrder).where(OrmOrder.id == id_)
                 .values(status=status, updated_at=datetime.now(UTC))
                 .returning(OrmOrder.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None


    """
        user_id: int | None = None
        status: OrderStatus | None = None
        status__in: set[OrderStatus] | None = None
        search: str | None = None
    """
    @staticmethod
    def _apply_filters(
            stmt: Select[tuple[OrmOrder]],
            query: OrderQuery,
    ) -> Select[tuple[OrmOrder]]:
        clauses = []
        if query.user_id is not None:
            column = get_column(stmt, "user_id")
            clauses.append(column == query.user_id)
        if query.status is not None:
            column = get_column(stmt, "status")
            clauses.append(column == query.status)
        if query.status__in is not None:
            column = get_column(stmt, "status")
            values = match_types(query.status__in, column)
            clauses.append(column.in_(values))
        if query.status__not_in is not None:
            column = get_column(stmt, "status")
            values = match_types(query.status__not_in, column)
            clauses.append(column.notin_(values))
        stmt = stmt.where(and_(*clauses))

        if query.search is not None:
            stmt = apply_search(stmt, query.search, list(map(str, OrderSearchBy)))

        return stmt


    async def get_many(self, query: OrderQueryPaged) -> QueryResult[Order]:
        stmt = select(OrmOrder)
        stmt = self._apply_filters(stmt, query)

        async with self.db.get_session() as session:
            total_items = await get_row_count(session, stmt)

            if query.sort_by is not None:
                stmt = apply_sorting(stmt, query.sort_by, query.sort)

            items, page, per_page, total_pages = [], None, None, None

            if query.page > 0 and query.per_page > 0 and total_items > 0:
                stmt = apply_pagination(stmt, query.page, query.per_page)
                orm_items = (await session.scalars(stmt)).all()
                items = TypeAdapter(list[Order]).validate_python(orm_items)

                page = query.page
                per_page = query.per_page
                total_pages = ceil(total_items / query.per_page)

            return QueryResult[Order](items=items,
                                      page=page,
                                      per_page=per_page,
                                      total_pages=total_pages,
                                      total_items=total_items)


    async def get_count(self, query: OrderQuery) -> int:
        stmt = select(OrmOrder)
        stmt = self._apply_filters(stmt, query)
        async with self.db.get_session() as session:
            return await get_row_count(session, stmt)


    async def get_count_by_status(self, query: OrderQuery) -> list[QueryCountItem[OrderStatus]]:
        column = OrmOrder.status
        stmt = select(column, func.count(column))
        query.status = None
        query.status__in = None
        stmt = self._apply_filters(stmt, query)
        stmt = stmt.group_by(column).order_by(column)
        async with self.db.get_session() as session:
            result = (await session.execute(stmt)).all()
            return [QueryCountItem[OrderStatus](value=item[0],
                                                count=item[1]) for item in result]
