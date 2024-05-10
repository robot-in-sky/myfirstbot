from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from myfirstbot.base.entities.query import Pagination, QueryFilter, Sorting
from myfirstbot.base.repo.sql.abs_repo import AbstractRepo
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.base.repo.sql.exc_mapper import exception_mapper
from myfirstbot.base.repo.sql.query_utils import apply_filters, apply_pagination, apply_sorting
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repo.pgsql.models.order import Order as _OrderOrm


class OrderRepo(AbstractRepo[Order, OrderCreate, OrderUpdate]):

    def __init__(self, database: Database) -> None:
        self.db = database

    @exception_mapper
    async def add(self, instance: OrderCreate) -> Order:
        query = (insert(_OrderOrm).values(**instance.model_dump())
                 .returning(_OrderOrm))
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            await session.commit()
            return Order.model_validate(result)

    async def get(self, id_: int) -> Order | None:
        query = select(_OrderOrm).where(_OrderOrm.id == id_)
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            return Order.model_validate(result) if result else None

    async def get_many(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> list[Order]:
        query = select(_OrderOrm)
        if filters:
            query = apply_filters(query, filters, or_=or_)
        if sorting:
            query = apply_sorting(query, sorting)
        if pagination:
            query = apply_pagination(query, pagination)
        async with self.db.get_session() as session:
            result = (await session.scalars(query)).all()
            return list(map(Order.model_validate, result))

    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        query = (update(_OrderOrm).where(_OrderOrm.id == id_)
                 .values(**instance.model_dump(), updated=datetime.now(UTC))
                 .returning(_OrderOrm))
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            if result:
                await session.commit()
                return Order.model_validate(result)
            return None

    async def delete(self, id_: int) -> int | None:
        query = delete(_OrderOrm).where(_OrderOrm.id == id_).returning(_OrderOrm.id)
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            if result:
                await session.commit()
                return result
            return None

    async def get_status(self, id_: int) -> OrderStatus | None:
        query = select(_OrderOrm.status).where(_OrderOrm.id == id_)
        async with self.db.get_session() as session:
            return await session.scalar(query)

    async def set_status(self, id_: int, status: OrderStatus) -> int | None:
        query = (update(_OrderOrm).where(_OrderOrm.id == id_)
                 .values(status=status, updated=datetime.now(UTC))
                 .returning(_OrderOrm.id))
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            if result:
                await session.commit()
                return result
            return None
