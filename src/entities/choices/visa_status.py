from enum import StrEnum, auto


class VisaStatus(StrEnum):
    DRAFT = auto()
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()
    TRASH = auto()
