from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entities.choices import Country, VisaStatus, VisaType
from src.repositories.orm_models import OrmBase


class OrmVisa(OrmBase):

    __tablename__ = "visas"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["OrmUser"] = relationship(lazy="selectin")  # noqa: F821
    country: Mapped["Country"] = mapped_column(Enum(Country))
    visa_type: Mapped["VisaType"] = mapped_column(Enum(VisaType))
    surname: Mapped[str] = mapped_column(Text)
    given_name: Mapped[str] = mapped_column(Text)
    passport_no: Mapped[str] = mapped_column(Text)
    form_data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    attachment_id: Mapped[UUID] = mapped_column(Uuid)
    status: Mapped["VisaStatus"] = mapped_column(Enum(VisaStatus), default=VisaStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
