import logging

from src.entities.base import QueryCountItem, QueryResult
from src.entities.choices import OrderStatus, UserRole
from src.entities.order import Order, OrderAdd, OrderQuery, OrderQueryPaged, OrderUpdate
from src.entities.user import User
from src.exceptions import AccessDeniedError, InvalidStateError, NotFoundError
from src.repositories.order_repo import OrderRepo
from src.repositories.utils import Database
from src.services.utils.access_level import access_level


class OrderService:

    def __init__(self, database: Database, current_user: User) -> None:
        self.order_repo = OrderRepo(database)
        self.current_user = current_user

    def _log(self, order: Order, message: str) -> None:
        logging.info(f"Order #{order.id} [@{self.current_user.user_name}]: {message}")

    @access_level(required=UserRole.USER)
    async def get_many(self, q: OrderQueryPaged) -> QueryResult[Order]:
        if self.current_user.role < UserRole.AGENT:
            if q.user_id != self.current_user.id:
                raise AccessDeniedError
            if q.status == OrderStatus.TRASH:
                raise AccessDeniedError
            q.status__not_in = q.status__not_in or set()
            q.status__not_in.add(OrderStatus.TRASH)
        return await self.order_repo.get_many(q)

    @access_level(required=UserRole.USER)
    async def get_count(self, q: OrderQuery) -> int:
        if self.current_user.role < UserRole.AGENT:
            if q.user_id != self.current_user.id:
                raise AccessDeniedError
            if q.status == OrderStatus.TRASH:
                raise AccessDeniedError
            q.status__not_in = q.status__not_in or set()
            q.status__not_in.add(OrderStatus.TRASH)
        return await self.order_repo.get_count(q)

    @access_level(required=UserRole.USER)
    async def get_count_by_status(self, q: OrderQuery) -> list[QueryCountItem[OrderStatus]]:
        q.status = None
        q.status__in = None
        q.status__not_in = None
        if self.current_user.role < UserRole.AGENT:
            if q.user_id != self.current_user.id:
                raise AccessDeniedError
            q.status__not_in = q.status__not_in or set()
            q.status__not_in.add(OrderStatus.TRASH)
        return await self.order_repo.get_count_by_status(q)

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
