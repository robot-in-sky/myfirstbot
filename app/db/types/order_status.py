import enum


class OrderStatus(enum.Enum):

    TRASH = 'TRASH'
    DRAFT = 'DRAFT'
    PENDING = 'PENDING'
    REVISION = 'REVISION'
    ACCEPTED = 'ACCEPTED'
    SUBMITTED = 'SUBMITTED'
    REJECTED = 'REJECTED'
    ARCHIVED = 'ARCHIVED'
