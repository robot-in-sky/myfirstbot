from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.query import Pagination, QueryResult, Sorting
from myfirstbot.entities.query.filters import ChoiceQueryFilter, NumQueryFilter
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, InvalidStateError, NotFoundError
from myfirstbot.repo.order import OrderRepo
from myfirstbot.repo.utils import Database
from myfirstbot.services.utils.access_level import access_level


class OrderService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.order_repo = OrderRepo(database)
        self.current_user = current_user

    @access_level(required=UserRole.USER)
    async def get_my(
            self,
            status: OrderStatus | None = None,
            page: int = 1,
            per_page: int = 10
    ) -> QueryResult[Order]:
        filters = [NumQueryFilter(field="user_id", type="eq", value=self.current_user.id)]
        if status:
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        else:
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_many(
            filters=filters,
            pagination=Pagination(page=page, per_page=per_page),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.AGENT)
    async def get_all(
            self,
            status: OrderStatus | None = None,
            user_id: int | None = None,
            page: int = 1,
            per_page: int = 10
    ) -> QueryResult[Order]:
        filters = []
        if user_id:
            filters.append(NumQueryFilter(field="user_id", type="eq", value=user_id))
        if status:
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        else:
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_many(
            filters=filters,
            pagination=Pagination(page=page, per_page=per_page),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.USER)
    async def new(self, instance: OrderAdd) -> Order:
        return await self.order_repo.add(instance)

    def _check_ownership(self, order: Order) -> None:
        if (self.current_user.role == UserRole.USER and
                order.user_id != self.current_user.id):
            raise AccessDeniedError

    @staticmethod
    def _check_status(order: Order, status: OrderStatus) -> None:
        if order.status != status:
            raise InvalidStateError

    @access_level(required=UserRole.USER)
    async def get(self, id_: int) -> Order:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            return order
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def update(self, id_: int, instance: OrderUpdate) -> Order:
        if order := await self.order_repo.update(id_, instance):
            self._check_ownership(order)
            return order
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def submit(self, id_: int) -> int | None:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            return await self.order_repo.set_status(id_, OrderStatus.PENDING)
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def return_(self, id_: int) -> int | None:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.PENDING)
            return await self.order_repo.set_status(id_, OrderStatus.DRAFT)
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def trash(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            return await self.order_repo.set_status(id_, OrderStatus.TRASH)
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def accept(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            return await self.order_repo.set_status(id_, OrderStatus.ACCEPTED)
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def reject(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            return await self.order_repo.set_status(id_, OrderStatus.DRAFT)
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def done(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.ACCEPTED)
            return await self.order_repo.set_status(id_, OrderStatus.COMPLETED)
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def restore(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            return await self.order_repo.set_status(id_, OrderStatus.DRAFT)
        raise NotFoundError

    @access_level(required=UserRole.ADMINISTRATOR)
    async def delete(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            return await self.order_repo.delete(id_)
        raise NotFoundError
