from datetime import UTC, datetime

from myfirstbot.base.entities.base import Base
from myfirstbot.entities.choices.order_status import OrderStatus


class OrderCreate(Base):
    user_id: int
    label: str
    size: int
    qty: int
    status: OrderStatus = OrderStatus.DRAFT
    created: datetime = datetime.now(UTC)
    updated: datetime = datetime.now(UTC)


class Order(Base):
    id: int
    user_id: int
    label: str
    size: int
    qty: int
    status: OrderStatus
    created: datetime
    updated: datetime


class OrderUpdate(Base):
    label: str | None = None
    size: int | None = None
    qty: int | None = None
    status: OrderStatus | None = None
    updated: datetime = datetime.now(UTC)

