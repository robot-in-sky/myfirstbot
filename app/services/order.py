import logging

from app.entities.choices import OrderStatus, UserRole
from app.entities.order import Order, OrderAdd, OrderUpdate
from app.entities.query import CountResultItem, Pagination, QueryResult, Search, Sorting
from app.entities.query.filters import ChoiceQueryFilter, NumQueryFilter, QueryFilter
from app.entities.user import User
from app.exceptions import AccessDeniedError, InvalidStateError, NotFoundError
from app.repo.order import OrderRepo
from app.repo.utils import Database
from app.services.utils.access_level import access_level


class OrderService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.order_repo = OrderRepo(database)
        self.search_fields = {"label"}
        self.current_user = current_user

    def _log(self, order: Order, message: str) -> None:
        logging.info(f"Order #{order.id} [@{self.current_user.user_name}]: {message}")

    @access_level(required=UserRole.USER)
    async def get_all(  # noqa: PLR0913
            self,
            user_id: int | None = None,
            status: OrderStatus | None = None,
            s: str | None = None,
            page: int = 1,
            per_page: int = 10,
    ) -> QueryResult[Order]:
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
        return await self.order_repo.get_all(
            filters=filters,
            search=Search(s=s, fields=self.search_fields) if s else None,
            pagination=Pagination(page=page, per_page=per_page),
            sorting=Sorting(order_by="created", sort="desc"),
        )

    @access_level(required=UserRole.USER)
    async def get_count(
            self,
            user_id: int | None = None,
            status: OrderStatus | None = None,
            s: str | None = None,
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
        return await self.order_repo.get_count(
            filters=filters,
            search=Search(s=s, fields=self.search_fields) if s else None,
        )

    @access_level(required=UserRole.USER)
    async def get_count_by_status(
            self,
            user_id: int | None = None,
            s: str | None = None,
    ) -> list[CountResultItem[OrderStatus]]:
        filters: list[QueryFilter] = []
        if user_id:
            if self.current_user.role < UserRole.AGENT and user_id != self.current_user.id:
                raise AccessDeniedError
            filters.append(NumQueryFilter(field="user_id", type="eq", value=user_id))
        if self.current_user.role < UserRole.AGENT:
            filters.append(ChoiceQueryFilter(field="status", type="isn", value=OrderStatus.TRASH))
        return await self.order_repo.get_count_by_status(
            filters=filters,
            search=Search(s=s, fields=self.search_fields) if s else None,
        )

    @access_level(required=UserRole.USER)
    async def new(self, instance: OrderAdd) -> Order:
        order = await self.order_repo.add(instance)
        self._log(order, "created")
        return order

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
            self._log(order, "updated")
            return order
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def submit(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            if await self.order_repo.set_status(id_, OrderStatus.PENDING):
                self._log(order, "submitted")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def return_(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                self._log(order, "returned")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.USER)
    async def trash(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_ownership(order)
            self._check_status(order, OrderStatus.DRAFT)
            if await self.order_repo.set_status(id_, OrderStatus.TRASH):
                self._log(order, "trashed")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def accept(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.ACCEPTED):
                self._log(order, "accepted")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def reject(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.PENDING)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                self._log(order, "rejected")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def done(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.ACCEPTED)
            if await self.order_repo.set_status(id_, OrderStatus.COMPLETED):
                self._log(order, "done")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def restore(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            if await self.order_repo.set_status(id_, OrderStatus.DRAFT):
                self._log(order, "restored")
                return order.id
        raise NotFoundError

    @access_level(required=UserRole.AGENT)
    async def delete(self, id_: int) -> int:
        if order := await self.order_repo.get(id_):
            self._check_status(order, OrderStatus.TRASH)
            if await self.order_repo.delete(id_):
                self._log(order, "deleted")
                return order.id
        raise NotFoundError
