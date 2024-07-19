from datetime import datetime

from app.entities.base import Base
from app.entities.choices import OrderStatus
from app.entities.user import User


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
    created: datetime
    updated: datetime


class OrderUpdate(Base):
    label: str | None = None
    size: int | None = None
    qty: int | None = None
