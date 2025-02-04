from uuid import UUID

from src.entities.base import Base
from src.entities.passport import PassportDetails


class RecognitionResult(Base):
    id: UUID
    type: str
    details: PassportDetails
