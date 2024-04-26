from sqlalchemy import BigInteger, Enum, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from myfirstbot.base.repositories.sql.models.base import Base
from myfirstbot.entities.enums.access_level import AccessLevel


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    access_level: Mapped["AccessLevel"] = mapped_column(
        Enum(AccessLevel), default=AccessLevel.USER
    )

