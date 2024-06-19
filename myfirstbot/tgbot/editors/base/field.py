from typing import Any

from pydantic import BaseModel


class Field(BaseModel):
    id: str
    name: str
    type: str
    text: str
    placeholder: str | None = None
    keyboard: dict[str, Any] | None = None
    kb_columns: int = 2
    validators: dict[str, Any] | None = None
