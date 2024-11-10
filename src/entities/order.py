from datetime import datetime
from typing import Literal

from src.entities.base import Base
from src.entities.choices import OrderStatus
from src.entities.user import User


class OrderAdd(Base):
    user_id: int
    label: str
    size: int
    qty: int


class Order(Base):
    id: int
    user_id: int
    user: User
    label: str
    size: int
    qty: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class OrderUpdate(Base):
    label: str | None = None
    size: int | None = None
    qty: int | None = None


class OrderQuery(Base):
    user_id: int | None = None
    status: OrderStatus | None = None
    status__in: set[OrderStatus] | None = None
    status__not_in: set[OrderStatus] | None = None
    search: str | None = None


class OrderQueryPaged(OrderQuery):
    sort_by: str | None = "created_at"
    sort: Literal["asc", "desc"] | None = "desc"
    page: int = 1
    per_page: int = 10


ORDER_SEARCH_BY = {"label"}
