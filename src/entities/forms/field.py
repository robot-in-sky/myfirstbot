from dataclasses import dataclass

from .choice import Choice
from .enums.field_type import FieldType


@dataclass
class Field:
    id: str
    name: str
    input_text: str
    examples: list[str] | None = None
    type: FieldType = FieldType.STR
    choice: Choice | None = None
    validators: list[str] | None = None
    hidden: bool = False
    depends_on: str | None = None
