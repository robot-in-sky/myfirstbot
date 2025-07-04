import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.entities.users import UserRole
from src.orm_models import OrmBase


class OrmUser(OrmBase):

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    user_name: Mapped[str] = mapped_column(Text)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    role: Mapped["UserRole"] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
