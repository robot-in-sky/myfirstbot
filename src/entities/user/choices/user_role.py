from enum import IntEnum, auto


class UserRole(IntEnum):
    BLOCKED = auto()
    USER = auto()
    AGENT = auto()
    ADMINISTRATOR = auto()
