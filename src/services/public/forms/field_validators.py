from collections.abc import Sequence
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, ValidationError as _ValidationError

from src.exceptions import ValidationError
from src.tgbot.utils.helpers import get_key_by_value


class ValidatorModel(BaseModel):
    int: int
    float: float

    str10: str = Field(max_length=10)
    str14: str = Field(max_length=14)
    str15: str = Field(max_length=15)
    str20: str = Field(max_length=20)
    str30: str = Field(max_length=30)
    str35: str = Field(max_length=35)
    str50: str = Field(max_length=50)
    str75: str = Field(max_length=75)
    str200: str = Field(max_length=200)

    eng_chars: str = Field(pattern=r"[a-zA-Z-]+")
    eng_chars_spaces: str = Field(pattern=r"[a-zA-Z-\s]+")
    eng_chars_digits_spaces: str = Field(pattern=r"[0-9a-zA-Z-\s]+")
    digits: str = Field(pattern=r"[0-9]+")
    digits_spaces: str = Field(pattern=r"[0-9\s]+")

    address: str = Field(pattern=r"[0-9a-zA-Z-.,/()']+")
    phone: str = Field(pattern=r"^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")


def apply_validators(value: Any, validators: Sequence[str]) -> None:
    try:
        model = ValidatorModel.model_construct()
        for validator in validators:
            ValidatorModel.__pydantic_validator__.validate_assignment(model, validator, value)
    except _ValidationError as error:
        message = "Ошибка валидации!"
        loc = error.errors()[0].get("loc")
        if loc:
            if loc[0] == "int" or loc[0] == "float":
                message = "Неверный формат числа"
            elif loc[0] == "phone":
                message = "Неверный формат номера"
            elif loc[0].startswith("str"):
                message = "Слишком много символов"
            elif loc[0].startswith("int") | loc[0].startswith("float"):
                message = "Некорректное значение"
            else:
                message = "Недопустимые символы"
        message += "\nПопробуйте снова"
        raise ValidationError(message) from None


def validate_date_input(field: Field, text: str) -> date:
    try:
        date_ = datetime.strptime(text, "%d.%m.%Y").date()  # noqa: DTZ007
    except ValueError:
        message = "Неверный формат даты"
        raise ValidationError(message) from None
    now = datetime.now().date()  # noqa: DTZ005
    diff = date_ - now
    month_diff = diff.days // 30
    year_diff = diff.days // 365
    message = "Неверное значение даты"
    match field.id:
        case "arrival_date":
            if not (0 <= month_diff <= 6):  # noqa: PLR2004
                raise ValidationError(message) from None
        case "birth_date":
            if not (-100 <= year_diff <= 0):  # noqa: PLR2004
                raise ValidationError(message) from None
        case "issue_date":
            if not (-20 <= year_diff <= 0):  # noqa: PLR2004
                raise ValidationError(message) from None
        case "expiry_date":
            if not (-20 <= year_diff <= 20):  # noqa: PLR2004
                raise ValidationError(message) from None
    return date_


def validate_choice_input(field: Field, text: str) -> Any:
    value = get_key_by_value(field.choice.output, text, text)
    if value not in field.choice.all:
        message = "Недопустимое значение"
        raise ValidationError(message) from None
    return value
