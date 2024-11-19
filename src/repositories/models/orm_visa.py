from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entities.choices import Country, Education, Gender, MartialStatus, Port, Religion, VisaStatus, VisaType
from src.repositories.models import OrmBase


class OrmVisa(OrmBase):

    __tablename__ = "visas"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["OrmUser"] = relationship(lazy="selectin")  # noqa: F821
    status: Mapped["VisaStatus"] = mapped_column(Enum(VisaStatus), default=VisaStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    # 1. REGISTRATION
    nationality: Mapped["Country"] = mapped_column(Enum(Country))
    visa_type: Mapped["VisaType"] = mapped_column(Enum(VisaType))
    entry_port: Mapped["Port"] = mapped_column(Enum(Port))
    arrival_date: Mapped[date] = mapped_column(Date())

    # 2. BASIC DETAILS
    # 2.1 Applicant Details
    surname: Mapped[str] = mapped_column(Text)
    given_name: Mapped[str] = mapped_column(Text)
    prev_surname: Mapped[str] = mapped_column(Text, nullable=True)
    prev_given_name: Mapped[str] = mapped_column(Text, nullable=True)
    gender: Mapped["Gender"] = mapped_column(Enum(Gender))
    birth_date: Mapped[date] = mapped_column(Date())
    birth_country: Mapped["Country"] = mapped_column(Enum(Country))
    birth_place: Mapped[str] = mapped_column(Text)
    national_id_no: Mapped[str] = mapped_column(Text)
    religion: Mapped["Religion"] = mapped_column(Enum(Religion))
    religion_other: Mapped[str] = mapped_column(Text, nullable=True)
    education: Mapped["Education"] = mapped_column(Enum(Education))
    prev_country: Mapped["Country"] = mapped_column(Enum(Country), nullable=True)
    # 2.2 Passport Details
    passport_no: Mapped[str] = mapped_column(Text)
    passport_issue_place: Mapped[str] = mapped_column(Text)
    passport_issue_date: Mapped[date] = mapped_column(Date())
    passport_expiry_date: Mapped[date] = mapped_column(Date())

    # 3. FAMILY DETAILS
    # 3.1 Address Details
    country: Mapped["Country"] = mapped_column(Enum(Country))
    state: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text)
    zipcode: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(Text)
    # 3.2 Family Details
    father_name: Mapped[str] = mapped_column(Text)
    father_nationality: Mapped["Country"] = mapped_column(Enum(Country))
    father_birth_country: Mapped["Country"] = mapped_column(Enum(Country))
    father_birth_place: Mapped[str] = mapped_column(Text)
    mother_name: Mapped[str] = mapped_column(Text)
    mother_nationality: Mapped["Country"] = mapped_column(Enum(Country))
    mother_birth_country: Mapped["Country"] = mapped_column(Enum(Country))
    mother_birth_place: Mapped[str] = mapped_column(Text)
    martial_status: Mapped["MartialStatus"] = mapped_column(Enum(MartialStatus))
