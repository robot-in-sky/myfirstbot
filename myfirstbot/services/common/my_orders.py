from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.query import Pagination, QueryResult, Sorting
from myfirstbot.entities.query.filters import ChoiceQueryFilter, NumQueryFilter
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, InvalidStateError
from myfirstbot.repo import OrderRepo
from myfirstbot.repo.utils import Database
from myfirstbot.services.utils.access_level import access_level


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


    async def get_all(self, per_page: int = 10, page: int = 1) -> QueryResult[Order]:
        return await self.order_repo.get_many(
            filters=[
                NumQueryFilter(field="user_id", type="eq", value=self.current_user.id),
                ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH),
            ],
            sorting=Sorting(order_by="created", sort="desc"),
            pagination=Pagination(page=page, per_page=per_page),
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
