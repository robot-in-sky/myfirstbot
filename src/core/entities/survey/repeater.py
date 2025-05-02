from dataclasses import dataclass

from .field import Field


@dataclass
class Repeater:
    id: str
    name: str
    description: str
    condition_field: Field
    repeater_fields: list[Field]
