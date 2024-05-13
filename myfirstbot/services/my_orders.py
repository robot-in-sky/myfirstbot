from myfirstbot.base.entities.query import ChoiceQueryFilter, NumQueryFilter, Pagination, Sorting
from myfirstbot.base.repo.sql.database import Database
from myfirstbot.base.services.access_level import access_level
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.choices.user_role import UserRole
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, InvalidStateError
from myfirstbot.repo.pgsql.order import OrderRepo


class MyOrdersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.order_repo = OrderRepo(database)
        self.current_user = current_user


    @access_level(required=UserRole.USER)
    async def new(self, instance: OrderAdd) -> Order:
        return await self.order_repo.add(instance)


    async def get(self, id_: int) -> Order:
        order = await self.order_repo.get(id_)
        if order and order.user_id == self.current_user.id:
            return order
        raise AccessDeniedError


    async def get_all(self, limit: int = 10, page: int = 1) -> list[Order]:
        return await self.order_repo.get_many(
            filters=[
                NumQueryFilter(field="user_id", type="eq", value=self.current_user.id),
                ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH),
            ],
            sorting=Sorting(order_by="created", sort="desc"),
            pagination=Pagination(page=page, page_size=limit),
        )


    @access_level(required=UserRole.USER)
    async def update(self, id_: int, instance: OrderUpdate) -> Order | None:
        order = await self.order_repo.get(id_)
        if order and order.user_id == self.current_user.id:
            if order.status == OrderStatus.DRAFT:
                return await self.order_repo.update(id_, instance)
            raise InvalidStateError
        raise AccessDeniedError


    @access_level(required=UserRole.USER)
    async def submit(self, id_: int) -> int | None:
        order = await self.order_repo.get(id_)
        if order and order.user_id == self.current_user.id:
            if order.status == OrderStatus.DRAFT:
                return await self.order_repo.set_status(id_, OrderStatus.PENDING)
            raise InvalidStateError
        raise AccessDeniedError


    @access_level(required=UserRole.USER)
    async def return_(self, id_: int) -> int | None:
        order = await self.order_repo.get(id_)
        if order and order.user_id == self.current_user.id:
            if order.status == OrderStatus.PENDING:
                return await self.order_repo.set_status(id_, OrderStatus.DRAFT)
            raise InvalidStateError
        raise AccessDeniedError


    async def trash(self, id_: int) -> int | None:
        order = await self.order_repo.get(id_)
        if order and order.user_id == self.current_user.id:
            if order.status == OrderStatus.DRAFT:
                return await self.order_repo.set_status(id_, OrderStatus.TRASH)
            raise InvalidStateError
        raise AccessDeniedError
