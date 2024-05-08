from myfirstbot.base.repo.sql.database import Database
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.repo.pgsql.order import OrderRepo


class UserService:
    def __init__(self, database: Database) -> None:
        session = database.get_session()
        self.repo = OrderRepo(session)

    async def add(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        age: int,
        status: OrderStatus = OrderStatus.DRAFT
    ) -> Order:
        return self.repo.add(OrderCreate(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            status=status
        ))

    async def get(self, id_: int) -> Order | None:
        return self.repo.get(id_)

    async def delete(self, id_: int) -> None:
        return self.repo.delete(id_)

    async def get_all(
            self,
            user_id: int | None,
            status: OrderStatus | None = None,
            *,
            skip: int = 0,
            limit: int = -1,
            order_by: str | None = None,
    ) -> list[Order]:
        return self.repo.get_all(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit,
            order_by=order_by,
        )

    async def set_status(
            self, id_: int, status: OrderStatus,
    ) -> Order:
        return await self.repo.update(
            id_, OrderUpdate(status=status)
        )
