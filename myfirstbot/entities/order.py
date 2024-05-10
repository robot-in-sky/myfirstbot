from datetime import datetime

from myfirstbot.base.entities.base import Base
from myfirstbot.entities.choices.order_status import OrderStatus


class OrderCreate(Base):
    user_id: int
    label: str
    size: int
    qty: int


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
