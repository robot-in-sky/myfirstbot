import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.entities.visas import AppFormStatus, Country

from .base import OrmBase


class OrmAppForm(OrmBase):

    __tablename__ = "app_forms"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    user: Mapped["OrmUser"] = relationship(lazy="selectin")  # noqa: F821
    country: Mapped["Country"] = mapped_column(Enum(Country))
    visa_id: Mapped[str] = mapped_column(String(64))
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    status: Mapped["AppFormStatus"] = mapped_column(Enum(AppFormStatus), default=AppFormStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
