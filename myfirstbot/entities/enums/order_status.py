from enum import StrEnum


class OrderStatus(StrEnum):
    TRASH = "TRASH"
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    REVISION = "REVISION"
    ACCEPTED = "ACCEPTED"
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
