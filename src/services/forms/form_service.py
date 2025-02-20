from src.entities.form import Choice, Field, FieldType, Form, Section

from . import choices
from .field_validators import apply_validators, validate_choice_input, validate_date_input


class FormService:
    def __init__(self) -> None:
        self._choices = [
            Choice(id="yes_no",
                   all=choices.yes_no.YES_NO,
                   featured=choices.yes_no.YES_NO,
                   output=choices.yes_no.YES_NO_OUTPUT),

            Choice(id="country",
                   all=choices.country.COUNTRY_ALL,
                   featured=choices.country.COUNTRY_FEATURED,
                   output=choices.country.COUNTRY_OUTPUT),

            Choice(id="gender",
                   all=choices.gender.GENDER,
                   featured=choices.gender.GENDER,
                   output=choices.gender.GENDER_OUTPUT),

            Choice(id="martial_status",
                   all=choices.martial_status.MARTIAL_STATUS_ALL,
                   featured=choices.martial_status.MARTIAL_STATUS_FEATURED,
                   output=choices.martial_status.MARTIAL_STATUS_OUTPUT),

            Choice(id="education_ind",
                   all=choices.education.EDUCATION_IND_ALL,
                   featured=choices.education.EDUCATION_IND_FEATURED,
                   output=choices.education.EDUCATION_IND_OUTPUT),

            Choice(id="port_ind",
                   all=choices.port.PORT_IND_ALL,
                   featured=choices.port.PORT_IND_FEATURED,
                   output=choices.port.PORT_IND_OUTPUT),

            Choice(id="religion_ind",
                   all=choices.religion.RELIGION_IND_ALL,
                   featured=choices.religion.RELIGION_IND_FEATURED,
                   output=choices.religion.RELIGION_IND_OUTPUT),
        ]

        self._fields = [
            # 1. REGISTRATION
            Field(id="nationality",
                  name="Гражданство",
                  input_text="Укажите гражданство (по паспорту)",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="entry_port",
                  name="Порт прибытия",
                  input_text="Выберите планируемый порт прибытия",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("port_ind")),

            Field(id="arrival_date",
                  name="Дата прибытия",
                  input_text="Выедите планируемую дату прибытия в формате ДД.ММ.ГГГГ",
                  type=FieldType.DATE),

            # 2. BASIC DETAILS
            # 2.1 Applicant Details
            Field(id="surname",
                  name="Фамилия",
                  input_text="Введите фамилию на английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="given_name",
                  name="Имя",
                  input_text="Введите имя на английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="prev_surname",
                  name="Предыдущая фамилия",
                  input_text="Введите предыдущую фамилию на английском",
                  validators=["str50", "eng_chars_spaces"],
                  is_optional=True,
                  condition_text="Менялась ли фамилия когда-либо?"),

            Field(id="prev_given_name",
                  name="Предыдущее имя",
                  input_text="Введите предыдущее имя на английском",
                  validators=["str50", "eng_chars_spaces"],
                  is_optional=True,
                  condition_text="Менялось ли имя когда-либо?"),

            Field(id="gender",
                  name="Пол",
                  input_text="Укажите пол",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("gender")),

            Field(id="birth_date",
                  name="Дата рождения",
                  input_text="Введите дату рождения в формате ДД.ММ.ГГГГ",
                  type=FieldType.DATE),

            Field(id="birth_country",
                  name="Страна рождения",
                  input_text="Укажите страну рождения",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="birth_place",
                  name="Место рождения",
                  input_text="Укажите место рождения:\n"
                             "только название города или региона на английском",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="national_id_no",
                  name="Внутренний документ",
                  input_text="Номер внутреннего идентифицирующего документа (внутреннего паспорта)",
                  validators=["str30", "eng_chars_digits_spaces"]),

            Field(id="religion_ind",
                  name="Религия",
                  input_text="Укажите религиозную принадлежность",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("religion_ind")),

            Field(id="education_ind",
                  name="Образование",
                  input_text="Укажите образование",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("education_ind")),

            Field(id="prev_nationality",
                  name="Предыдущее гражданство",
                  input_text="Укажите предыдущее гражданство",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country"),
                  is_optional=True,
                  condition_text="Менялось ли гражданство когда-либо?"),

            # 2.2 Passport Details
            Field(id="passport_no",
                  name="Номер паспорта",
                  input_text="Укажите номер паспорта (загран)",
                  validators=["str14", "digits_spaces"]),

            Field(id="passport_issue_place",
                  name="Место выдачи",
                  input_text="Укажите место выдачи паспорта на английском",
                  validators=["str20", "eng_chars_digits_spaces"]),

            Field(id="passport_issue_date",
                  name="Дата выдачи",
                  input_text="Укажите дату выдачи паспорта в формате ДД.ММ.ГГГГ",
                  type=FieldType.DATE),

            Field(id="passport_expiry_date",
                  name="Дата окончания",
                  input_text="Укажите дату окончания срока действия паспорта в формате ДД.ММ.ГГГГ",
                  type=FieldType.DATE),

            # 3. FAMILY DETAILS
            # 3.1 Address Details
            Field(id="country",
                  name="Страна проживания",
                  input_text="Укажите страну проживания",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="state",
                  name="Регион",
                  input_text="Введите название региона на английском",
                  validators=["str35", "eng_chars_digits_spaces"]),

            Field(id="address",
                  name="Адрес",
                  input_text="Введите адрес проживания на английском",
                  validators=["str35", "address"]),

            Field(id="zipcode",
                  name="Индекс",
                  input_text="Укажите почтовый индекс",
                  validators=["str15", "digits"]),

            Field(id="phone",
                  name="Номер телефона",
                  input_text="Введите номер телефона",
                  validators=["str15", "phone"]),

            # 3.2 Family Details
            Field(id="father_name",
                  name="Имя отца",
                  input_text="Введите имя отца на английском",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="father_nationality",
                  name="Гражданство отца",
                  input_text="Укажите гражданство отца",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="father_birth_country",
                  name="Страна рождения отца",
                  input_text="Укажите страну рождения отца",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="father_birth_place",
                  name="Место рождения отца",
                  input_text="Укажите место рождения отца:\n"
                             "только название города или региона на английском",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="mother_name",
                  name="Имя матери",
                  input_text="Введите имя матери на английском",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="mother_nationality",
                  name="Гражданство матери",
                  input_text="Укажите гражданство матери",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="mother_birth_country",
                  name="Страна рождения матери",
                  input_text="Укажите страну рождения матери",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country")),

            Field(id="mother_birth_place",
                  name="Место рождения матери",
                  input_text="Укажите место рождения матери:\n"
                             "только название города или региона на английском",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="martial_status",
                  name="Семейное положение",
                  input_text="Укажите семейное положение",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("martial_status")),
        ]

        self._sections = [
            Section(id="registration",
                    name="Регистрационные данные",
                    fields=[
                        self.get_field("nationality"),
                        self.get_field("entry_port"),
                        self.get_field("arrival_date"),
                    ]),

            Section(id="applicant_details",
                    name="Данные заявителя",
                    fields=[
                        self.get_field("surname"),
                        self.get_field("given_name"),
                        self.get_field("prev_surname"),
                        self.get_field("prev_given_name"),
                        self.get_field("gender"),
                        self.get_field("birth_date"),
                        self.get_field("birth_country"),
                        self.get_field("birth_place"),
                        self.get_field("national_id_no"),
                        self.get_field("religion_ind"),
                        self.get_field("education_ind"),
                        self.get_field("prev_nationality"),
                    ]),

            Section(id="passport_details",
                    name="Данные паспорта",
                    fields=[
                        self.get_field("passport_no"),
                        self.get_field("passport_issue_place"),
                        self.get_field("passport_issue_date"),
                        self.get_field("passport_expiry_date"),
                    ]),

            Section(id="address_details",
                    name="Данные о месте проживания",
                    fields=[
                        self.get_field("country"),
                        self.get_field("state"),
                        self.get_field("address"),
                        self.get_field("zipcode"),
                        self.get_field("phone"),
                    ]),

            Section(id="family_details",
                    name="Данные о семье",
                    fields=[
                        self.get_field("martial_status"),
                        self.get_field("father_name"),
                        self.get_field("father_nationality"),
                        self.get_field("father_birth_country"),
                        self.get_field("father_birth_place"),
                        self.get_field("mother_name"),
                        self.get_field("mother_nationality"),
                        self.get_field("mother_birth_country"),
                        self.get_field("mother_birth_place"),
                    ]),
        ]

        self._forms = [
            Form(id="ind_tour", name="Туристическая виза в Индию",
                 sections=[
                     self.get_section("registration"),
                     self.get_section("applicant_details"),
                     self.get_section("passport_details"),
                     self.get_section("address_details"),
                     self.get_section("family_details"),
                 ]),
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
    def validate_input(field: Field, text: str) -> str:
        value = text.strip()
        match field.type:
            case FieldType.DATE:
                date_value = validate_date_input(field, value)
                value = str(date_value)
            case FieldType.CHOICE:
                choice_value = validate_choice_input(field, value)
                value = str(choice_value)
            case _:
                validators = field.validators or []
                apply_validators(value, validators)
        return value


    def get_condition_field(self, field: Field, id_: str | None = None ) -> Field:
        default_id = f"{field.id}_condition"
        name = f"{field.name}?"
        return Field(
            id=id_ or default_id,
            name=name,
            input_text=field.condition_text,
            type=FieldType.CHOICE,
            choice=self.get_choice("yes_no"))
