from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column as _col

from myfirstbot.base.repo.sql.models.base import Base
from myfirstbot.entities.enums.access_level import AccessLevel


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = _col(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = _col(BigInteger, unique=True)
    user_name: Mapped[str] = _col(Text)
    first_name: Mapped[str] = _col(Text, nullable=True)
    last_name: Mapped[str] = _col(Text, nullable=True)
    chat_id: Mapped[int] = _col(BigInteger, nullable=True)
    access_level: Mapped["AccessLevel"] = _col(Enum(AccessLevel), default=AccessLevel.USER)
    created: Mapped[datetime] = _col(DateTime(timezone=True), default=func.now())
    updated: Mapped[datetime] = _col(DateTime(timezone=True), default=func.now())
