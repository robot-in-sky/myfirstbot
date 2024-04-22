from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.repositories.abs_repo import AbstractRepo
from myfirstbot.base.repositories.exc_mapper import exception_mapper
from myfirstbot.entities.enums.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repositories.postgresql.models.order import Order as OrderModel


class OrderRepo(AbstractRepo[Order]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.session = session
        self.model = OrderModel

    @exception_mapper
    async def add(self, instance: OrderCreate) -> Order:
        attrs = instance.model_dump()
        statement = insert(self.model).values(**attrs).returning(self.model)
        result = self.session.execute(statement)
        return Order.model_validate(result)

    @exception_mapper
    async def get(self, id_: int) -> Order | None:
        instance = await self.session.get(self.model, id_)
        return Order.model_validate(instance) if instance else None

    @exception_mapper
    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        values = instance.model_dump()
        statement = (update(self.model).where(self.model.id == id_)
                     .values(**values).returning(self.model))
        result = self.session.execute(statement)
        return Order.model_validate(result)

    @exception_mapper
    async def delete(self, ident: int) -> None:
        if instance := self.session.get(self.model, ident):
            await self.session.delete(instance)
            await self.session.commit()

    # @exception_mapper
    # async def get_one(self, **filter_by) -> Order | None:
    #     statement = select(self.model).filter_by(**filter_by)
    #     result = await self.session.scalar(statement)
    #     return Order.model_validate(result) if result else None

    @exception_mapper
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by: str | None = None, **filter_by,
    ) -> list[Order]:
        statement = select(self.model).filter_by(**filter_by)
        statement = statement.offset(skip).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)
        result = (await self.session.scalars(statement)).all()
        return list(map(Order.model_validate, result))

    async def set_status(self, ident: int, status: OrderStatus) -> Order | None:
        return await self.update(ident, status=status)
