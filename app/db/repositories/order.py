from sqlalchemy.ext.asyncio import AsyncSession

from .abs_repo import AbstractRepo
from .abs_orm_repo import AbstractOrmRepo
from .exc_mapper import exception_mapper

from ..models.order import OrderModel
from ..schemas.order import OrderSchemaAdd, OrderSchema
from ..types.order_status import OrderStatus


class OrderRepo(AbstractRepo[OrderSchema]):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.orm = AbstractOrmRepo[OrderModel](session=session, model=OrderModel)

    @exception_mapper
    async def add(self, instance: OrderSchemaAdd) -> OrderSchema:
        instance = await self.orm.add(**instance.model_dump())
        return OrderSchema.model_validate(instance)

    @exception_mapper
    async def get(self, ident: int) -> OrderSchema | None:
        instance = await self.orm.get(ident)
        return OrderSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def get_one(self, **filter_by) -> OrderSchema | None:
        instance = await self.orm.get_one(**filter_by)
        return OrderSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by=None, **filter_by
    ) -> list[OrderSchema]:
        instances = await self.orm.get_many(
            skip=skip, limit=limit, order_by=order_by, **filter_by
        )
        return list(map(OrderSchema.model_validate, instances))

    @exception_mapper
    async def update(self, ident: int, **attrs) -> OrderSchema | None:
        for k, v in attrs.items():
            OrderSchema.__pydantic_validator__.validate_assignment(
                OrderSchema.model_construct(), k, v
            )
        instance = await self.orm.update(ident=ident, **attrs)
        return OrderSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def delete(self, ident: int) -> None:
        await self.orm.delete(ident)

    async def get_many_by_user_id(
            self, user_id: int, skip: int = 0, limit: int = 100, order_by=None
    ) -> list[OrderSchema]:
        return await self.get_many(
            user_id=user_id, skip=skip, limit=limit, order_by=order_by
        )

    async def set_status(self, ident: int, status: OrderStatus) -> OrderSchema | None:
        return await self.update(ident, status=status)
