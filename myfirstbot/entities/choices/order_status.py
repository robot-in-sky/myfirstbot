from enum import StrEnum, auto


class OrderStatus(StrEnum):
    TRASH = auto()
    DRAFT = auto()
    PENDING = auto()
    ACCEPTED = auto()
    COMPLETED = auto()
