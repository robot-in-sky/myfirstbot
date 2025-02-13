from datetime import date, datetime
from enum import StrEnum, auto
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import StringConstraints

from src.entities.base import Base
from src.entities.form import Country, EducationInd, Gender, MartialStatus, PortInd, ReligionInd
from src.entities.user import User

from .choices.visa_country import VisaCountry
from .choices.visa_status import VisaStatus
from .choices.visa_type import VisaType

Str14 = Annotated[str, StringConstraints(max_length=14)]
Str15 = Annotated[str, StringConstraints(max_length=15)]
Str20 = Annotated[str, StringConstraints(max_length=20)]
Str30 = Annotated[str, StringConstraints(max_length=30)]
Str35 = Annotated[str, StringConstraints(max_length=35)]
Str50 = Annotated[str, StringConstraints(max_length=50)]


class VisaBase(Base):
    country: VisaCountry
    visa_type: VisaType
    attachment_id: UUID
    form_data: dict[str, Any]


class FormDataInd(Base):

    # 1. REGISTRATION
    nationality: Country
    visa_type: VisaType
    entry_port: PortInd
    arrival_date: date

    # 2. BASIC DETAILS
    # 2.1 Applicant Details
    surname: Str50
    given_name: Str50
    prev_surname: Str50 | None
    prev_given_name: Str50 | None
    gender: Gender
    birth_date: date
    birth_country: Country
    birth_place: Str50
    national_id_no: Str30
    religion: ReligionInd
    religion_other: Str20 | None
    education: EducationInd
    prev_country: Country | None
    # 2.2 Passport Details
    passport_no: Str14
    passport_issue_place: Str20
    passport_issue_date: date
    passport_expiry_date: date

    # 3. FAMILY DETAILS
    # 3.1 Address Details
    country: Country
    state: Str35
    address: Str35
    zipcode: Str15
    phone: Str15
    # 3.2 Family Details
    father_name: Str50
    father_nationality: Country
    father_birth_country: Country
    father_birth_place: Str50
    mother_name: Str50
    mother_nationality: Country
    mother_birth_country: Country
    mother_birth_place: Str50
    martial_status: MartialStatus


class VisaAdd(VisaBase):
    user_id: int


class Visa(VisaBase):
    id: int
    user_id: int
    user: User
    status: VisaStatus
    created_at: datetime
    updated_at: datetime


class VisaUpdate(VisaBase):
    attachment_id: UUID | None = None
    form_data: dict[str, Any] | None = None


class VisaQuery(Base):
    user_id: int | None = None
    status: VisaStatus | None = None
    status__in: set[VisaStatus] | None = None
    status__not_in: set[VisaStatus] | None = None
    search: str | None = None


class VisaQueryPaged(VisaQuery):
    sort_by: str | None = "created_at"
    sort: Literal["asc", "desc"] | None = "desc"
    page: int = 1
    per_page: int = 10


class VisaSearchBy(StrEnum):
    FORM_DATA = auto()


__all__ = [
    "VisaCountry",
    "VisaType",
    "VisaStatus",
    "VisaAdd",
    "Visa",
    "VisaUpdate",
    "VisaQuery",
    "VisaQueryPaged",
    "VisaSearchBy",
]
