import logging

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.repo.sql.abs_repo import AbstractRepo
from myfirstbot.base.repo.sql.exc_mapper import exception_mapper
from myfirstbot.entities.enums.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repo.pgsql.models.order import Order as _OrderOrm


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


    @exception_mapper
    async def get_all(
        self,
        user_id: int | None,
        status: OrderStatus | None = None,
        *,
        skip: int = 0,
        limit: int = -1,
        order_by: str | None = None,
    ) -> list[Order]:
        query = select(_OrderOrm)
        if user_id:
            query = query.where(_OrderOrm.user_id == user_id)
        if status:
            query = query.where(_OrderOrm.status == status)
        if limit > 0:
            query = query.offset(skip).limit(limit)
        if order_by:
            query = query.order_by(order_by)
        result = (await self.session.scalars(query)).all()
        return list(map(Order.model_validate, result))
