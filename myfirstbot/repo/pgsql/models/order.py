from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column as _col

from myfirstbot.base.repo.sql.models.base import Base
from myfirstbot.entities.enums.order_status import OrderStatus


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = _col(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = _col(Integer, ForeignKey("users.id"))
    label: Mapped[str] = _col(Text)
    size: Mapped[int] = _col(Integer)
    qty: Mapped[int] = _col(Integer)
    status: Mapped["OrderStatus"] = _col(Enum(OrderStatus), default=OrderStatus.DRAFT)
    created: Mapped[datetime] = _col(DateTime(timezone=True), default=func.now())
    updated: Mapped[datetime] = _col(DateTime(timezone=True), default=func.now())
