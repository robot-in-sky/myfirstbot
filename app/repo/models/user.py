from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.entities.choices import UserRole
from app.repo.models import OrmBase


class OrmUser(OrmBase):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    role: Mapped["UserRole"] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
