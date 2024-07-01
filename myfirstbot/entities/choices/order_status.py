from enum import StrEnum, auto


class OrderStatus(StrEnum):
    DRAFT = auto()
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()
    TRASH = auto()
