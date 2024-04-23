import logging

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.repositories.sqlalchemy.abs_repo import AbstractRepo
from myfirstbot.base.repositories.sqlalchemy.exc_mapper import exception_mapper
from myfirstbot.entities.enums.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repositories.postgresql.models.order import Order as _OrderOrm


class OrderRepo(AbstractRepo[Order, OrderCreate, OrderUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @exception_mapper
    async def add(self, instance: OrderCreate) -> Order:
        values = instance.model_dump()
        query = insert(_OrderOrm).values(**values).returning(_OrderOrm)
        result = await self.session.scalar(query)
        logging.info(result)
        await self.session.commit()
        return Order.model_validate(result)

    @exception_mapper
    async def get(self, id_: int) -> Order | None:
        query = select(_OrderOrm).where(_OrderOrm.id == id_)
        result = await self.session.scalar(query)
        return Order.model_validate(result) if result else None

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

    async def set_status(self, id_: int, status: OrderStatus) -> Order | None:
        return await self.update(id_, OrderUpdate(status=status))


"""
    @exception_mapper
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by: str | None = None, **filter_by,
    ) -> list[Order]:
        statement = select(_OrderOrm).filter_by(**filter_by)
        statement = statement.offset(skip).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)
        result = (await self.session.scalars(statement)).all()
        return list(map(Order.model_validate, result))
"""
