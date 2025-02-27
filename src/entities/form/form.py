from dataclasses import dataclass
from enum import Enum, StrEnum, auto


class FieldType(StrEnum):
    STR = auto()
    DATE = auto()
    CHOICE = auto()


@dataclass
class Choice:
    id: str
    all: list[Enum | str]
    featured: list[Enum | str]
    output: dict[Enum | str, str]


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


@dataclass
class Repeater:
    id: str
    name: str
    description: str
    condition_field: Field
    repeater_fields: list[Field]


@dataclass
class Section:
    id: str
    name: str
    fields: list[Field]


@dataclass
class Form:
    id: str
    name: str
    sections: list[Section | Repeater]
