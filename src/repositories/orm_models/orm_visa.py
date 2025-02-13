from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entities.visa import VisaCountry, VisaStatus, VisaType
from src.repositories.orm_models import OrmBase


class OrmVisa(OrmBase):

    __tablename__ = "visas"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["OrmUser"] = relationship(lazy="selectin")  # noqa: F821
    country: Mapped["VisaCountry"] = mapped_column(Enum(VisaCountry))
    visa_type: Mapped["VisaType"] = mapped_column(Enum(VisaType))
    attachment_id: Mapped[UUID] = mapped_column(Uuid)
    form_data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    status: Mapped["VisaStatus"] = mapped_column(Enum(VisaStatus), default=VisaStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
