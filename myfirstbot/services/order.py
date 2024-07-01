from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.query import CountedResultItem, Pagination, QueryResult, Sorting
from myfirstbot.entities.query.filters import ChoiceQueryFilter, NumQueryFilter, QueryFilter
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
    async def get_all(
            self,
            user_id: int | None = None,
            status: OrderStatus | None = None,
            page: int = 1,
            per_page: int = 10
    ) -> QueryResult[Order]:
        filters: list[QueryFilter] = []
        if user_id:
            if self.current_user.role < UserRole.AGENT and user_id != self.current_user.id:
                raise AccessDeniedError
            filters.append(NumQueryFilter(field="user_id", type="eq", value=user_id))
        if status:
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        else:
            if self.current_user.role < UserRole.AGENT and status == OrderStatus.TRASH:
                raise AccessDeniedError
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_all(
            filters=filters,
            pagination=Pagination(page=page, per_page=per_page),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.USER)
    async def get_count(
            self,
            user_id: int | None = None,
            status: OrderStatus | None = None,
    ) -> int:
        filters: list[QueryFilter] = []
        if user_id:
            if self.current_user.role < UserRole.AGENT and user_id != self.current_user.id:
                raise AccessDeniedError
            filters.append(NumQueryFilter(field="user_id", type="eq", value=user_id))
        if status:
            if self.current_user.role < UserRole.AGENT and status == OrderStatus.TRASH:
                raise AccessDeniedError
            filters.append(ChoiceQueryFilter(field="status", type="is", value=status))
        else:
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_count(filters=filters)

    @access_level(required=UserRole.USER)
    async def get_count_by_status(
            self,
            user_id: int | None = None,
    ) -> list[CountedResultItem[OrderStatus]]:
        filters: list[QueryFilter] = []
        if user_id:
            if self.current_user.role < UserRole.AGENT and user_id != self.current_user.id:
                raise AccessDeniedError
            filters.append(NumQueryFilter(field="user_id", type="eq", value=user_id))
        if self.current_user.role < UserRole.AGENT:
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_count_by_status(filters=filters)

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
    async def submit(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            if await self.order_repo.set_status(id_, OrderStatus.PENDING):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def return_(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def trash(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            if await self.order_repo.set_status(id_, OrderStatus.TRASH):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def accept(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.ACCEPTED):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def reject(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def done(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.ACCEPTED)
            if await self.order_repo.set_status(id_, OrderStatus.COMPLETED):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def restore(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def delete(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            if await self.order_repo.delete(id_):
                return order.id
        raise NotFoundError
