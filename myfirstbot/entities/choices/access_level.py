from enum import IntEnum


class AccessLevel(IntEnum):
    BLOCKED = -1
    USER = 0
    AGENT = 1
    ADMINISTRATOR = 2
