from myfirstbot.base.entities.query import NumQueryFilter, Pagination, Sorting
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.exceptions import InvalidStateError
from myfirstbot.repo.pgsql.order import OrderRepo


class UserOrdersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.orders = OrderRepo(database)
        self.current_user = current_user


    async def new(self, instance: OrderCreate) -> Order:
        return await self.orders.add(instance)


    async def get(self, id_: int) -> Order:
        return await self.orders.get(id_)


    async def get_all(self) -> list[Order]:
        return await self.orders.get_many(
            filters=[NumQueryFilter(field="user_id", type="eq", value=self.current_user.id)],
            sorting=Sorting(order_by="created", sort="desc"),
            pagination=Pagination(page=1, page_size=20),
        )


    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        if await self.orders.get_status(id_) == OrderStatus.DRAFT:
            return await self.orders.update(id_, instance)
        raise InvalidStateError


    async def trash(self, id_: int) -> int | None:
        if await self.orders.get_status(id_) == OrderStatus.DRAFT:
            return await self.orders.set_status(id_, OrderStatus.TRASH)
        raise InvalidStateError
