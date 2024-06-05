from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.order import Order, OrderUpdate
from myfirstbot.entities.query import Pagination, QueryResult, Sorting
from myfirstbot.entities.query.filters import ChoiceQueryFilter, NumQueryFilter
from myfirstbot.entities.user import User
from myfirstbot.exceptions import InvalidStateError, NotFoundError
from myfirstbot.repo.order import OrderRepo
from myfirstbot.repo.utils import Database
from myfirstbot.services.utils.access_level import access_level


class ManageOrdersService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.order_repo = OrderRepo(database)
        self.current_user = current_user

    @access_level(required=UserRole.AGENT)
    async def get(self, id_: int) -> Order:
        if order := await self.order_repo.get(id_):
            return order
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def get_by_user(self, user_id: int, page: int = 1) -> QueryResult[Order]:
        return await self.order_repo.get_many(
            filters=[NumQueryFilter(field="user_id", type="eq", value=user_id)],
            pagination=Pagination(page=page, per_page=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.AGENT)
    async def get_all(
            self, status: OrderStatus | None = None, page: int = 1,
    ) -> QueryResult[Order]:
        filters = []
        if status:
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        return await self.order_repo.get_many(
            filters=filters,
            pagination=Pagination(page=page, per_page=10),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.AGENT)
    async def update(self, id_: int, instance: OrderUpdate) -> Order:
        if order := await self.order_repo.update(id_, instance):
            return order
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def accept(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            if order.status == OrderStatus.PENDING:
                await self.order_repo.set_status(id_, OrderStatus.ACCEPTED)
            raise InvalidStateError
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def reject(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            if order.status == OrderStatus.PENDING:
                return await self.order_repo.set_status(id_, OrderStatus.DRAFT)
            raise InvalidStateError
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def done(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            if order.status == OrderStatus.ACCEPTED:
                return await self.order_repo.set_status(id_, OrderStatus.COMPLETED)
            raise InvalidStateError
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def trash(self, id_: int) -> int:
        if result := await self.order_repo.set_status(id_, OrderStatus.TRASH):
            return result
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def restore(self, id_: int) -> int:
        if result := await self.order_repo.set_status(id_, OrderStatus.DRAFT):
            return result
        raise NotFoundError

    @access_level(required=UserRole.ADMINISTRATOR)
    async def delete(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            if order.status == OrderStatus.TRASH:
                return await self.order_repo.delete(id_)
            raise InvalidStateError
        raise NotFoundError
