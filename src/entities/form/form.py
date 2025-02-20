from dataclasses import dataclass
from enum import Enum, StrEnum, auto


class FieldType(StrEnum):
    STR = auto()
    DATE = auto()
    CHOICE = auto()


@dataclass
class Choice:
    id: str
    all: list[Enum]
    featured: list[Enum]
    output: dict[Enum, str]


@dataclass
class Field:
    id: str
    name: str
    input_text: str
    type: FieldType = FieldType.STR
    choice: Choice | None = None
    validators: list[str] | None = None
    is_optional: bool = False
    condition_text: str | None = None


@dataclass
class Section:
    id: str
    name: str
    fields: list[Field]


@dataclass
class Repeater:
    id: str
    name: str
    condition_text: str
    fields: list[Field]


@dataclass
class Form:
    id: str
    name: str
    sections: list[Section | Repeater]
