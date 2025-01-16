from datetime import date

from src.entities.base import Base
from src.entities.choices import Gender


class PassportDetails(Base):
    surname: str | None
    given_name: str | None
    passport_no: str | None
    country: str | None
    birth_date: date | None
    gender: Gender | None
    birth_place: str | None
    issue_date: date | None
    expire_date: date | None


class PassportAttachments(Base):
    source: str
    scanned: str | None
    photo: str | None
    debug: str | None
