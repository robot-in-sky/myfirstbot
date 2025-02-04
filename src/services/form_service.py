from src.entities.forms import Field, Form, Section
from src.exceptions import ValidationError


class FormService:
    def __init__(self) -> None:
        self._fields = [
            Field(id="given_name", name="Имя", input_text="Ваше имя",
                  type="text", validators={"max_len": 20}),
            Field(id="surname", name="Имя", input_text="Ваша фамилия",
                  type="text", validators={"max_len": 20}),
            Field(id="country", name="Гражданство", input_text="Ваше гражданство",
                  type="text", validators={"in": ["Россия", "Казахстан", "Беларусь"]},
                  kb_options={"Россия": "RUS", "Казахстан": "KAZ", "Беларусь": "BLR"}, kb_columns=3),
            Field(id="brothers", name="Кол-во братьев", input_text="Сколько у вас братьев?", type="int",
                  validators={"min": 0, "max": 20}),
        ]

        self._sections = [
            Section(id="passport_details",
                    name="Паспортные данные",
                    fields=[self.get_field("given_name"),
                            self.get_field("surname")]),
            Section(id="address_details",
                    name="Данные о месте проживания",
                    fields=[self.get_field("country")]),
            Section(id="family_details",
                    name="Данные о семье",
                    fields=[self.get_field("brothers")]),
        ]

        self._forms = [
            Form(id="ind_tour", name="Туристическая виза в Индию",
                 sections=[self.get_section("passport_details"),
                           self.get_section("address_details"),
                           self.get_section("family_details")]),
        ]

    def get_field(self, id_: str) -> Field:
        return next(filter(lambda f: f.id == id_, self._fields))

    def get_section(self, id_: str) -> Section:
        return next(filter(lambda f: f.id == id_, self._sections))

    def get_form(self, id_: str) -> Form:
        return next(filter(lambda f: f.id == id_, self._forms))

    @property
    def forms(self) -> list[Form]:
        return self._forms

    async def validate_input(self, f: Field, text: str) -> None:
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
                    if max_value and value > max_value:
                        err_msg = f"Максимальное значение {max_value}."
                        raise ValidationError(err_msg)

                case _:
                    err_msg = "Неизвестный тип поля"
                    raise ValueError(err_msg)

            allowed_values = f.validators.get("in")
            if allowed_values and value not in allowed_values:
                err_msg = f"Значение {value}. Допустимые значения {allowed_values}."
                raise ValidationError(err_msg)
