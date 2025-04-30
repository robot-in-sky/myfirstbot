from enum import StrEnum, auto


class AppFormStatus(StrEnum):
    DRAFT = auto()
    SAVED = auto()
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()
    TRASH = auto()
