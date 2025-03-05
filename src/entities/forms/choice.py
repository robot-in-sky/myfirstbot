from dataclasses import dataclass
from enum import Enum


@dataclass
class Choice:
    id: str
    all: list[Enum | str]
    featured: list[Enum | str]
    output: dict[Enum | str, str]
