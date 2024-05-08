from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from myfirstbot.base.repo.sql.models.base import Base
from myfirstbot.entities.choices.access_level import AccessLevel


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    access_level: Mapped["AccessLevel"] = mapped_column(Enum(AccessLevel), default=AccessLevel.USER)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now())
