from sqlalchemy import Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from myfirstbot.base.repositories.models.base import Base
from myfirstbot.entities.enums.order_status import OrderStatus


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped["OrderStatus"] = mapped_column(Enum(OrderStatus), default=OrderStatus.DRAFT)

