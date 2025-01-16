from datetime import timedelta
from enum import StrEnum, auto
from uuid import UUID

from src.entities.base import Base
from src.entities.passport import PassportAttachments, PassportDetails


class RecognitionRequest(Base):
    id: UUID
    timestamp: int
    type: str
    source: str


class RecognitionStatus(StrEnum):
    SUCCESS = auto()
    ERROR = auto()


class RecognitionResponse(Base):
    request_id: UUID
    request_timestamp: int
    type: str
    status: RecognitionStatus
    message: str
    duration: timedelta | None
    details: PassportDetails | None = None
    attachments: PassportAttachments | None = None
