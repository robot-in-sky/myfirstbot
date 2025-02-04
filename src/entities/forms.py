from typing import Any

from pydantic import BaseModel

from src.entities.choices import Country, VisaType


class Field(BaseModel):
    id: str
    name: str
    type: str
    input_text: str
    # placeholder: str | None = None
    kb_options: dict[str, Any] | None = None
    kb_columns: int = 2
    validators: dict[str, Any] | None = None


class Section(BaseModel):
    id: str
    name: str
    fields: list[Field]


class Form(BaseModel):
    id: str
    name: str
    sections: list[Section]


class VisaForm(Form):
    country: Country
    visa_type: VisaType
