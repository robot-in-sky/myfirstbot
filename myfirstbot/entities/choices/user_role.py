from enum import IntEnum


class UserRole(IntEnum):
    BLOCKED = -1
    USER = 0
    AGENT = 1
    ADMINISTRATOR = 2
