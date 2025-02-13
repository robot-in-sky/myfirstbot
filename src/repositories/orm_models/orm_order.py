from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entities.order import OrderStatus
from src.repositories.orm_models import OrmBase


class OrmOrder(OrmBase):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["OrmUser"] = relationship(lazy="selectin")  # noqa: F821
    label: Mapped[str] = mapped_column(Text)
    size: Mapped[int] = mapped_column(Integer)
    qty: Mapped[int] = mapped_column(Integer)
    status: Mapped["OrderStatus"] = mapped_column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
