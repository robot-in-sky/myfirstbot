from dataclasses import dataclass
from enum import Enum


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
    is_date: bool = False
    choice: Choice | None = None
    validators: list[str] | None = None


@dataclass
class Section:
    id: str
    name: str
    fields: list[Field]


@dataclass
class Form:
    id: str
    name: str
    sections: list[Section]
