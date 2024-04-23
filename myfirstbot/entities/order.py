from myfirstbot.base.entities.base import Base
from myfirstbot.entities.enums.order_status import OrderStatus


class OrderCreate(Base):
    user_id: int
    first_name: str
    last_name: str
    age: int
    status: OrderStatus = OrderStatus.DRAFT


class Order(Base):
    id: int
    user_id: int
    first_name: str
    last_name: str
    age: int
    status: OrderStatus


class OrderUpdate(Base):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    status: OrderStatus | None = None

