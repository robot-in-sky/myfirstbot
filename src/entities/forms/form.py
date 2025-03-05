from dataclasses import dataclass

from .repeater import Repeater
from .section import Section


@dataclass
class Form:
    id: str
    name: str
    sections: list[Section | Repeater]
