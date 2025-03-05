from dataclasses import dataclass

from .field import Field


@dataclass
class Section:
    id: str
    name: str
    fields: list[Field]
