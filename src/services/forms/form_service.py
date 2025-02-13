from src.entities.form import Choice, Field, Form, Section
from src.tgbot.utils.helpers import get_key_by_value

from . import choices
from .field_validator import validate_field


class FormService:
    def __init__(self) -> None:
        self._choices = [
            Choice(id="country",
                   all=choices.country.COUNTRY_ALL,
                   default=choices.country.COUNTRY_DEFAULT,
                   output=choices.country.COUNTRY_OUTPUT),

            Choice(id="gender",
                   all=choices.gender.GENDER_ALL,
                   default=choices.gender.GENDER_DEFAULT,
                   output=choices.gender.GENDER_OUTPUT),

            Choice(id="martial_status",
                   all=choices.martial_status.MARTIAL_STATUS_ALL,
                   default=choices.martial_status.MARTIAL_STATUS_DEFAULT,
                   output=choices.martial_status.MARTIAL_STATUS_OUTPUT),

            Choice(id="education_ind",
                   all=choices.education.EDUCATION_IND_ALL,
                   default=choices.education.EDUCATION_IND_DEFAULT,
                   output=choices.education.EDUCATION_IND_OUTPUT),

            Choice(id="port_ind",
                   all=choices.port.PORT_IND_ALL,
                   default=choices.port.PORT_IND_DEFAULT,
                   output=choices.port.PORT_IND_OUTPUT),

            Choice(id="religion_ind",
                   all=choices.religion.RELIGION_IND_ALL,
                   default=choices.religion.RELIGION_IND_DEFAULT,
                   output=choices.religion.RELIGION_IND_OUTPUT),
        ]

        self._fields = [
            Field(id="surname",
                  name="Фамилия",
                  input_text="Введите фамилию на английском, как в загранпаспорте",
                  validators=["str20", "eng"]),

            Field(id="given_name",
                  name="Имя",
                  input_text="Введите имя на английском, как в загранпаспорте",
                  validators=["str20", "eng"]),

            Field(id="gender",
                  name="Пол",
                  input_text="Укажите пол",
                  choice=self.get_choice("gender")),

            Field(id="nationality",
                  name="Гражданство",
                  input_text="Гражданство по паспорту",
                  choice=self.get_choice("country")),

            Field(id="birth_date",
                  name="Дата рождения",
                  input_text="Введите дату рождения в формате ДД.ММ.ГГГГ",
                  validators = ["birth_date"]),

            Field(id="nationality",
                  name="Гражданство",
                  input_text="Гражданство по паспорту",
                  choice=self.get_choice("country")),

            Field(id="mother_name",
                  name="Имя матери",
                  input_text="Введите имя матери на английском",
                  validators=["str20", "eng"]),
        ]

        self._sections = [
            Section(id="passport_details",
                    name="Паспортные данные",
                    fields=[self.get_field("given_name"),
                            self.get_field("surname"),
                            self.get_field("gender")]),

            Section(id="address_details",
                    name="Данные о месте проживания",
                    fields=[self.get_field("nationality")]),

            Section(id="family_details",
                    name="Данные о семье",
                    fields=[self.get_field("mother_name")]),
        ]

        self._forms = [
            Form(id="ind_tour", name="Туристическая виза в Индию",
                 sections=[self.get_section("passport_details"),
                           self.get_section("address_details"),
                           self.get_section("family_details")]),
        ]

    def get_choice(self, id_: str) -> Choice:
        return next(filter(lambda e: e.id == id_, self._choices))

    def get_field(self, id_: str) -> Field:
        return next(filter(lambda e: e.id == id_, self._fields))

    def get_section(self, id_: str) -> Section:
        return next(filter(lambda e: e.id == id_, self._sections))

    def get_form(self, id_: str) -> Form:
        return next(filter(lambda e: e.id == id_, self._forms))


    @staticmethod
    def validate_field_input(field: Field, text: str) -> str:
        value = text.strip()
        validators = []
        if field.choice:
            value = get_key_by_value(field.choice.output, value, value)
            validators.append(field.choice.id)
        if field.validators:
            validators.extend(field.validators)
        validate_field(value, validators)
        return value
