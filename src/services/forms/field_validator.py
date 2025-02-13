from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, Field, FutureDate, PastDate, ValidationError as _ValidationError

from src.entities.form import Country, EducationInd, Gender, MartialStatus, PortInd, ReligionInd
from src.exceptions import ValidationError


class ValidatorModel(BaseModel):
    eng: str = Field(pattern=r"[a-zA-Z]+")
    str14: str = Field(max_length=14)
    str15: str = Field(max_length=15)
    str20: str = Field(max_length=20)
    str30: str = Field(max_length=30)
    str35: str = Field(max_length=35)
    str50: str = Field(max_length=50)

    # TODO: add timedelta checking
    arrival_date: FutureDate    # 0 <= timedelta.month <= 6
    birth_date: PastDate   # 0 <= timedelta.year <= 100
    passport_issue_date: PastDate   # 0 <= timedelta.year <= 20
    passport_expire_date: FutureDate    # -20 <= timedelta.year <= 20

    country: Country
    gender: Gender
    martial_status: MartialStatus
    education_ind: EducationInd
    port_ind: PortInd
    religion_ind: ReligionInd


def validate_field(value: Any, validators: Sequence[str]) -> None:
    try:
        model = ValidatorModel.model_construct()
        for validator in validators:
            ValidatorModel.__pydantic_validator__.validate_assignment(model, validator, value)
    except _ValidationError as error:
        locs = []
        for e in error.errors():
            locs.extend(e["loc"])
        locs =  set(locs)
        lines = []
        for loc in locs:
            match loc:
                case "eng":
                    lines.append("Только английские символы")
                case "str14" | "str15" | "str20" | "str30" | "str35" | "str50":
                    lines.append("Слишком много символов")
                case "arrival_date" | "birth_date" | "passport_issue_date" | "passport_expire_date":
                    lines.append("Неверный формат даты")
                case "country" | "gender" | "martial_status" | "education_ind" | "port_ind" | "religion_ind":
                    lines.append("Значение не из списка")
                case _:
                    lines.append("Ошибка валидации!")
        lines.append("Попробуйте снова")
        error_message = "\n".join(lines)
        raise ValidationError(error_message) from None
