from datetime import date
from enum import StrEnum

from src.entities.base import Base

from .enums.country import Country
from .enums.gender import Gender


class PassportDetails(Base):
    surname: str | None
    given_name: str | None
    passport_no: str | None
    country: Country | None
    birth_date: date | None
    gender: Gender | None
    birth_place: str | None
    issue_date: date | None
    expiry_date: date | None



class PassportFiles(StrEnum):
    SOURCE = "source.png"
    SCANNED = "scanned.png"
    PHOTO = "photo.png"
    DEBUG = "debug.png"
