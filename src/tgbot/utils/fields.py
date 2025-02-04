from typing import Any

from pydantic import BaseModel

from src.exceptions import ValidationError


class Field(BaseModel):
    id: str
    name: str
    type: str
    input_text: str
    placeholder: str | None = None
    kb_options: dict[str, Any] | None = None
    kb_columns: int = 2
    validators: dict[str, Any] | None = None


class FormSection(BaseModel):
    id: str
    name: str
    fields: list[Field]


async def validate_field_input(f: Field, text: str) -> None:
    if f.validators:
        value: str | int
        match f.type:
            case "text":
                value = text
                max_len = f.validators.get("max_len")
                if max_len and len(value) > max_len:
                    err_msg = f"Длина не более {max_len} символов."
                    raise ValidationError(err_msg)

            case "int":
                try:
                    value = int(text)
                except (TypeError, ValueError):
                    err_msg = "Неверный формат."
                    raise ValidationError(err_msg) from None

                min_value = f.validators.get("min")
                if min_value and value < min_value:
                    err_msg = f"Минимальное значение {min_value}."
                    raise ValidationError(err_msg)

                max_value = f.validators.get("max")
                if max_value and value > max_value :
                    err_msg = f"Максимальное значение {max_value}."
                    raise ValidationError(err_msg)

            case _:
                err_msg = "Неизвестный тип поля"
                raise ValueError(err_msg)

        allowed_values = f.validators.get("in")
        if allowed_values and value not in allowed_values:
            err_msg = f"Значение {value}. Допустимые значения {allowed_values}."
            raise ValidationError(err_msg)
