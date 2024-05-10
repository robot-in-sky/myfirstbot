from myfirstbot.base.entities.query import ChoiceQueryFilter, NumQueryFilter, Pagination, Sorting
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.choices.user_role import UserRole
from myfirstbot.entities.order import Order, OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, InvalidStateError
from myfirstbot.repo.pgsql.order import OrderRepo


class DashboardOrdersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.orders = OrderRepo(database)
        self.current_user = current_user


    async def get(self, id_: int) -> Order:
        return await self.orders.get(id_)


    async def get_by_user(self, user_id: int, page: int = 1) -> list[Order]:
        return await self.orders.get_many(
            filters=[NumQueryFilter(field="user_id", type="eq", value=user_id)],
            pagination=Pagination(page=page, page_size=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )


    async def get_all(
            self, status: OrderStatus | None = None, page: int = 1,
    ) -> list[Order]:
        filters = []
        if status:
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        return await self.orders.get_many(
            filters=filters,
            pagination=Pagination(page=page, page_size=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )


    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        return await self.orders.update(id_, instance)


    async def reject(self, id_: int) -> int | None:
        if self.orders.get_status(id_) == OrderStatus.PENDING:
            return await self.orders.set_status(id_, OrderStatus.DRAFT)
        raise InvalidStateError


    async def accept(self, id_: int) -> int | None:
        if self.orders.get_status(id_) == OrderStatus.PENDING:
            return await self.orders.set_status(id_, OrderStatus.ACCEPTED)
        raise InvalidStateError


    async def done(self, id_: int) -> int | None:
        if self.orders.get_status(id_) == OrderStatus.ACCEPTED:
            return await self.orders.set_status(id_, OrderStatus.COMPLETED)
        raise InvalidStateError


    async def trash(self, id_: int) -> int | None:
        return await self.orders.set_status(id_, OrderStatus.TRASH)


    async def delete(self, id_: int) -> int | None:
        if self.current_user == UserRole.ADMINISTRATOR:
            return await self.orders.delete(id_)
        raise AccessDeniedError
