from sqlalchemy import Integer, BigInteger, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from app.db.types.access_level import AccessLevel


class UserModel(BaseModel):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    access_level: Mapped['AccessLevel'] = mapped_column(Enum(AccessLevel), default=AccessLevel.USER)
    # orders: Mapped[list['OrderModel']] = relationship(back_populates='user', lazy='selectin')

