from core.entities.survey import Choice, Field, FieldType, Repeater, Section, Survey

from . import choices
from .field_formatters import format_value
from .field_validators import apply_validators, validate_choice_input, validate_date_input


class SurveyService:
    def __init__(self) -> None:
        self._choices = [
            Choice(id="yes_no",
                   all=choices.yes_no.YES_NO,
                   featured=choices.yes_no.YES_NO,
                   output=choices.yes_no.YES_NO_OUTPUT),

            Choice(id="country_ind",
                   all=choices.country.COUNTRY_IND,
                   featured=choices.country.COUNTRY_FEATURED,
                   output=choices.country.COUNTRY_OUTPUT),

            Choice(id="country_all",
                   all=choices.country.COUNTRY_ALL,
                   featured=choices.country.COUNTRY_FEATURED2,
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

            Choice(id="saarc_country",
                   all=choices.country.COUNTRY_SAARC,
                   featured=choices.country.COUNTRY_SAARC,
                   output=choices.country.COUNTRY_OUTPUT),

            Choice(id="saarc_year",
                   all=choices.saarc_visit.SAARC_YEAR,
                   featured=choices.saarc_visit.SAARC_YEAR,
                   output=choices.saarc_visit.SAARC_YEAR_OUTPUT),

            Choice(id="saarc_visit_num",
                   all=choices.saarc_visit.SAARC_VISIT_NUM,
                   featured=choices.saarc_visit.SAARC_VISIT_NUM,
                   output=choices.saarc_visit.SAARC_VISIT_NUM_OUTPUT),

            Choice(id="old_visa_type",
                   all=choices.old_visa_type.OLD_VISA_IND,
                   featured=choices.old_visa_type.OLD_VISA_IND,
                   output=choices.old_visa_type.OLD_VISA_IND_OUTPUT),
        ]

        self._fields = [

            # REGISTRATION

            Field(id="nationality",
                  name="Гражданство",
                  input_text="Укажите гражданство (по паспорту)",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="entry_port",
                  name="Порт прибытия",
                  input_text="Выберите планируемый порт прибытия",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("port_ind")),

            Field(id="arrival_date",
                  name="Дата прибытия",
                  input_text="<b>Дата прибытия</b>:\n"
                             "Укажите планируемую дату в формате <code>ДД.ММ.ГГГГ</code>",
                  type=FieldType.DATE),

            # BASIC DETAILS
            # Applicant Details

            Field(id="surname",
                  name="Фамилия",
                  input_text="<b>Фамилия</b>:\n"
                             "Введите фамилию английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="given_name",
                  name="Имя",
                  input_text="<b>Имя</b>:\n"
                             "Введите имя на английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="_prev_surname_cond",
                  name="Предыдущая фамилия?",
                  input_text="Менялась ли фамилия когда-либо?",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no"),
                  hidden=True),

            Field(id="prev_surname",
                  name="Предыдущая фамилия",
                  input_text="<b>Предыдущая фамилия</b>:\n"
                             "Введите фамилию английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"],
                  depends_on="_prev_surname_cond"),

            Field(id="_prev_given_name_cond",
                  name="Предыдущее имя?",
                  input_text="Менялось ли имя когда-либо?",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no"),
                  hidden=True),

            Field(id="prev_given_name",
                  name="Предыдущее имя",
                  input_text="<b>Предыдущее имя</b>:\n"
                             "Введите имя английском, как в паспорте",
                  validators=["str50", "eng_chars_spaces"],
                  depends_on="_prev_given_name_cond"),

            Field(id="gender",
                  name="Пол",
                  input_text="Укажите пол",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("gender")),

            Field(id="birth_date",
                  name="Дата рождения",
                  input_text="<b>Дата рождения</b>:\n"
                             "Введите дату формате <code>ДД.ММ.ГГГГ</code>",
                  type=FieldType.DATE),

            Field(id="birth_country",
                  name="Страна рождения",
                  input_text="Укажите страну рождения",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="birth_place",
                  name="Место рождения",
                  input_text="<b>Место рождения</b>:\n"
                             "Укажите название города или региона. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Санкт-Петербург",
                            "Республика Башкортостан",
                            "Свердловская область",
                            "Краснодарский край",
                            "Chelyabinsk region"],
                  formatter="place_ru",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="national_id_no",
                  name="Внутренний документ",
                  input_text="<b>Внутренний документ</b>:\n"
                             "Укажите номер идентифицирующего документа (внутреннего паспорта)",
                  validators=["str30", "eng_chars_digits_spaces"]),

            Field(id="religion_ind",
                  name="Религия",
                  input_text="Укажите религиозную принадлежность",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("religion_ind")),

            Field(id="religion_other",
                  name="Религия (другое)",
                  input_text="<b>Религия (другое)</b>:\n"
                             "Укажите религиозную принадлежность на английском. "
                             "Можно указать <code>No</code>",
                  examples=["Ezid", "Agnostic", "No"],
                  validators=["str20", "eng_chars_digits_spaces"],
                  depends_on="religion_ind",
                  hidden=True),

            Field(id="education_ind",
                  name="Образование",
                  input_text="Укажите образование",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("education_ind")),

            Field(id="_prev_nationality_cond",
                  name="Предыдущее гражданство?",
                  input_text="Менялось ли гражданство когда-либо?",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no"),
                  hidden=True),

            Field(id="prev_nationality",
                  name="Предыдущее гражданство",
                  input_text="Укажите предыдущее гражданство",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind"),
                  depends_on="_prev_nationality_cond"),

            # Passport Details

            Field(id="passport_no",
                  name="Номер паспорта",
                  input_text="Укажите номер паспорта (загран)",
                  validators=["str14", "digits_spaces"]),

            Field(id="passport_issue_place",
                  name="Место выдачи",
                  input_text="<b>Место выдачи паспорта</b>:\n"
                             "Введите название города или региона. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Москва",
                            "Санкт-Петербург",
                            "Свердловская область",
                            "Краснодарский край",
                            "Chelyabinsk region"],
                  formatter="place_ru",
                  validators=["str20", "eng_chars_digits_spaces"]),

            Field(id="passport_issue_date",
                  name="Дата выдачи",
                  input_text="<b>Дата выдачи паспорта</b>:\n"
                             "Введите дату формате <code>ДД.ММ.ГГГГ</code>",
                  type=FieldType.DATE),

            Field(id="passport_expiry_date",
                  name="Дата окончания",
                  input_text="<b>Дата окончания срока действия паспорта</b>\n"
                             "Введите дату формате <code>ДД.ММ.ГГГГ</code>",
                  type=FieldType.DATE),

            # Address Details

            Field(id="country",
                  name="Страна проживания",
                  input_text="Укажите страну проживания",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="city",
                  name="Город",
                  input_text="<b>Город проживания</b>:\n"
                             "Можно указать областной центр\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Москва",
                            "Алматы",
                            "Нижний Тагил",
                            "Dubai"],
                  formatter="place_ru",
                  validators=["str35", "eng_chars_digits_spaces"]),

            Field(id="state",
                  name="Регион",
                  input_text="<b>Регион проживания</b>:\n"
                             "Укажите название региона. Можно на русском.\n\n"
                             "Текст будет автоматически преобразован в английский\n\n"
                             "Обратите внимание:\n"
                             "<code>Москва</code>, <code>Санкт-Петербург</code> "
                             "и <code>Севастополь</code> — это города федерального значения.\n"
                             "Вместо региона указываем название города",
                  examples=["Костанайская область",
                            "Краснодарский край",
                            "Севастополь",
                            "Antalya"],
                  formatter="place_ru",
                  validators=["str35", "eng_chars_digits_spaces"]),

            Field(id="address",
                  name="Адрес",
                  input_text="<b>Адрес проживания</b>:\n"
                             "Введите адрес проживания. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["ул. Красных Фонарей, 4-21",
                            "с. Калиновка, ул. Азина, 77",
                            "Lenina st. 41, apt. 88"],
                  formatter="address_ru",
                  validators=["str35", "address"]),

            Field(id="zipcode",
                  name="Индекс",
                  input_text="<b>Почтовый индекс\n</b>"
                             "Укажите почтовый индекс по месту проживания",
                  validators=["str15", "digits"]),

            Field(id="phone",
                  name="Номер телефона",
                  input_text="<b>Номер телефона</b>:\n"
                             "Введите номер в формате <code>+7XXXXXXXXXX</code>",
                  validators=["str15", "phone"]),

            # Family Details

            Field(id="father_name",
                  name="Имя отца",
                  input_text="<b>Имя отца</b>:\n"
                             "Введите имя. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Иван", "Юрий", "Nikolay"],
                  formatter="text_ru",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="father_nationality",
                  name="Гражданство отца",
                  input_text="Укажите гражданство отца",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="father_birth_country",
                  name="Страна рождения отца",
                  input_text="Укажите страну рождения отца",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="father_birth_place",
                  name="Место рождения отца",
                  input_text="<b>Укажите место рождения отца</b>:\n"
                             "Только название города или региона. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Москва",
                            "Санкт-Петербург",
                            "Свердловская область",
                            "Краснодарский край",
                            "Chelyabinsk region"],
                  formatter="place_ru",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="mother_name",
                  name="Имя матери",
                  input_text="<b>Имя матери</b>:\n"
                             "Введите имя. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Вера", "Надежда", "Lyubov"],
                  formatter="text_ru",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="mother_nationality",
                  name="Гражданство матери",
                  input_text="Укажите гражданство матери",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="mother_birth_country",
                  name="Страна рождения матери",
                  input_text="Укажите страну рождения матери",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_ind")),

            Field(id="mother_birth_place",
                  name="Место рождения матери",
                  input_text="<b>Место рождения матери</b>:\n"
                             "Укажите название города или региона. Можно на русском\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["Москва",
                            "Санкт-Петербург",
                            "Свердловская область",
                            "Краснодарский край",
                            "Chelyabinsk region"],
                  formatter="place_ru",
                  validators=["str50", "eng_chars_digits_spaces"]),

            Field(id="martial_status",
                  name="Семейное положение",
                  input_text="Укажите семейное положение",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("martial_status")),

            # Details of Visa Sought

            Field(id="places_to_be_visited",
                  name="Места посещения",
                  input_text="<b>Планируемые места посещения в Индии</b>\n\n"
                             "Перечислите названия штатов/городов через запятую\n\n"
                             "Желательно использовать оригинальные названия на английском",
                  examples=["Mumbai, Varanasi, Rishikesh",
                            "Goa, Hampi, Kerala",
                            "Дели, Агра, Джайпур"],
                  formatter="places_ind",
                  validators=["str50", "address"]),

            Field(id="exit_point",
                  name="Порт отбытия",
                  input_text="<b>Планируемый порт отбытия</b>:\n"
                             "Укажите, из какого порта планируется покидать Индию",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("port_ind")),

            # Old Visa Details

            Field(id="old_visa_cond",
                  name="Предыдущий визит",
                  input_text="<b>Предыдущий визит</b>:\n"
                             "Посещали Индию ранее?",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no")),

            Field(id="prev_visit_address1",
                  name="Предыдущий адрес 1",
                  input_text="<b>Предыдущий адрес</b>:\n"
                             "Укажите город/штат, где вы проживали в Индии\n\n"
                             "Желательно использовать оригинальные названия на английском",
                  examples=["Goa", "Mumbai", "Rishikesh, Uttarakhand", "Manali, Himachal Pradesh"],
                  formatter="places_ind",
                  validators=["str35", "address"],
                  depends_on="old_visa_cond"),

            Field(id="prev_visit_address2",
                  name="Предыдущий адрес 2",
                  input_text="<b>Предыдущий адрес</b>:\n"
                             "Укажите адрес или название отеля на английском\n\n"
                             "Адрес можно посмотреть на <a href='https://www.google.com/maps/'>Google-картах</a>",
                  examples=["God's Gift Guest House, Arambol"],
                  validators=["str35", "address"],
                  depends_on="old_visa_cond"),

            Field(id="visited_cities",
                  name="Посещённые города",
                  input_text="<b>Ранее посещённые города в Индии</b>\n"
                             "Перечислите названия городов/штатов через запятую\n\n"
                             "Места Гоа можно не указывать, просто укажите <code>Goa</code>\n\n"
                             "Желательно использовать оригинальные названия на английском",
                  examples=["Mumbai, Varanasi, Rishikesh",
                            "Goa, Hampi, Kerala",
                            "Дели, Агра, Джайпур"],
                  formatter="places_ind",
                  validators=["str75", "address"],
                  depends_on="old_visa_cond"),

            Field(id="old_visa_no",
                  name="Номер предыдущей визы",
                  input_text="<b>Предыдущая виза</b>:\n"
                             "Укажите номер визы\n\n"
                             "Номер указан на штампе или вклейке в паспорте",
                  examples=["VI7654321"],
                  validators=["str10", "eng_chars_digits_spaces"],
                  depends_on="old_visa_cond"),

            Field(id="old_visa_type",
                  name="Тип предыдущей визы",
                  input_text="<b>Предыдущая виза</b>:\n"
                             "Укажите тип визы",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("old_visa_type"),
                  depends_on="old_visa_cond"),

            Field(id="old_visa_issue_place",
                  name="Место выдачи",
                  input_text="<b>Предыдущая виза</b>:\n"
                             "Укажите место выдачи",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("port_ind"),
                  depends_on="old_visa_cond"),
                  # Should be converted to string

            Field(id="old_visa_issue_date",
                  name="Дата выдачи",
                  input_text="<b>Предыдущая виза</b>:\n"
                             "Укажите дату выдачи в формате <code>ДД.ММ.ГГГГ</code>",
                  type=FieldType.DATE,
                  depends_on="old_visa_cond"),

            # Other Information

            Field(id="_country_visit_cond",
                  name="Посещённые страны за 10 лет",
                  input_text="Были ли посещения каких-либо стран за последние 10 лет?\n"
                             "(кроме страны проживания)",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no")),

            Field(id="visited_country",
                  name="Страна",
                  input_text="Укажите страну",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("country_all")),

            # SAARC Country Visit Details

            Field(id="_saarc_country_visit_cond",
                  name="Посещения стран SAARC за 3 года",
                  input_text="<b>SAARC</b> – Южно-Азиатская ассоциация регионального сотрудничества\n\n"
                             "Кроме Индии, к странам SAARC относятся:\n\n"
                             f"{choices.saarc_visit.SAARC_LIST_TEXT}\n\n"
                             "<b>Были ли посещения стран SAARC за последние 3 года (кроме Индии)?</b>\n\n"
                             f"Для каждой страны необходимо будет указать год и количество посещений, "
                             f"если были несколько раз за год",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("yes_no"),
                  hidden=False),

            Field(id="saarc_country",
                  name="Страна",
                  input_text="Укажите страну",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("saarc_country")),

            Field(id="saarc_year",
                  name="Год",
                  input_text="Укажите год посещения",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("saarc_year")),

            Field(id="saarc_visit_num",
                  name="Количество посещений",
                  input_text="Укажите количество посещений",
                  type=FieldType.CHOICE,
                  choice=self.get_choice("saarc_visit_num")),

            # References

            Field(id="ref_name_home",
                  name="Имя",
                  input_text="<b>Контактное лицо</b>: Имя\n"
                             "Контактное лицо – представитель, друг или родственник в стране проживания\n\n"
                             "Укажите имя. Можно на русском",
                  examples=["Владимир", "Кайрат", "Svetlana"],
                  formatter="text_ru",
                  validators=["str50", "eng_chars_spaces"]),

            Field(id="ref_address_home",
                  name="Адрес",
                  input_text="<b>Контактное лицо</b>: Адрес\n"
                             "Укажите адрес. Можно указать любой адрес, это формальность\n\n"
                             "Текст будет автоматически преобразован в английский",
                  examples=["г. Краснозаводск, ул. Инженерной Мысли, 33"],
                  formatter="address_ru",
                  validators=["str200", "address"]),

            Field(id="ref_phone_home",
                  name="Номер телефона",
                  input_text="<b>Контактное лицо: Номер телефона</b>\n"
                             "Укажите номер телефона в формате <code>+7XXXXXXXXXX</code>",
                  validators=["str15", "phone"]),

            Field(id="ref_address_ind",
                  name="Адрес",
                  input_text="<b>Представитель в Индии</b>:\n"
                             "Укажем в качестве принимающей стороны отель/гест-хаус, "
                             "в котором планируется размещение\n\n"
                             "Укажите название и адрес отеля на английском\n\n"
                             "Адрес можно посмотреть на <a href='https://www.google.com/maps/'>Google-картах</a>",
                  examples=["Ivon Guest House, Girkarwado, Arambol, Pernem, Goa 403524"],
                  validators=["str200", "address"]),

            Field(id="ref_phone_ind",
                  name="Номер телефона",
                  input_text="<b>Представитель в Индии</b>:\n"
                             "Укажите номер телефона отеля в формате <code>+91XXXXXXXXXX</code>\n\n"
                             "Номер телефона можно также посмотреть на <a href='https://www.google.com/maps/'>Google-картах</a>",
                  validators=["str15", "phone"]),

        ]

        self._sections = [
            Section(id="__passport_details__",
                    name="Данные паспорта",
                    fields=[
                        self.get_field("nationality"),
                        self.get_field("passport_no"),
                        self.get_field("surname"),
                        self.get_field("given_name"),
                        self.get_field("gender"),
                        self.get_field("birth_date"),
                        self.get_field("birth_country"),
                        self.get_field("birth_place"),
                        self.get_field("passport_issue_place"),
                        self.get_field("passport_issue_date"),
                        self.get_field("passport_expiry_date"),
                    ]),

            Section(id="applicant_details",
                    name="Данные заявителя",
                    fields=[
                        self.get_field("national_id_no"),
                        self.get_field("_prev_surname_cond"),
                        self.get_field("prev_surname"),
                        self.get_field("_prev_given_name_cond"),
                        self.get_field("prev_given_name"),
                        self.get_field("_prev_nationality_cond"),
                        self.get_field("prev_nationality"),
                        self.get_field("education_ind"),
                        self.get_field("religion_ind"),
                        self.get_field("religion_other"),
                    ]),

            Section(id="address_details",
                    name="Место проживания",
                    fields=[
                        self.get_field("country"),
                        self.get_field("city"),
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

            Section(id="visa_details",
                    name="Текущий визит в Индию",
                    fields=[
                        self.get_field("entry_port"),
                        self.get_field("arrival_date"),
                        self.get_field("places_to_be_visited"),
                        self.get_field("exit_point"),
                    ]),

            Section(id="previous_visa_details",
                    name="Предыдущий визит в Индию",
                    fields=[
                        self.get_field("old_visa_cond"),
                        self.get_field("prev_visit_address1"),
                        self.get_field("prev_visit_address2"),
                        self.get_field("visited_cities"),
                        self.get_field("old_visa_no"),
                        self.get_field("old_visa_type"),
                        self.get_field("old_visa_issue_place"),
                        self.get_field("old_visa_issue_date"),
                    ]),

            Repeater(id="visited_countries",
                     name="Посещённые страны",
                     description="Перечислите все посещенные страны за последние 10 лет",
                     condition_field=self.get_field("_country_visit_cond"),
                     repeater_fields=[
                         self.get_field("visited_country"),
                     ]),

            Repeater(id="saarc_country_visits",
                     name="Посещёния стран SAARC",
                     description="Перечислите посещения стран SAARC за последние 3 года",
                     condition_field=self.get_field("_saarc_country_visit_cond"),
                     repeater_fields=[
                         self.get_field("saarc_country"),
                         self.get_field("saarc_year"),
                         self.get_field("saarc_visit_num"),
                     ]),

            Section(id="reference_details_home",
                    name="Представитель в стране проживания",
                    fields=[
                        self.get_field("ref_name_home"),
                        self.get_field("ref_address_home"),
                        self.get_field("ref_phone_home"),
                    ]),

            Section(id="reference_details_ind",
                    name="Представитель в Индии",
                    fields=[
                        self.get_field("ref_address_ind"),
                        self.get_field("ref_phone_ind"),
                    ]),
        ]

        self._surveys = [
            Survey(id="ind_tour", name="Туристическая виза в Индию",
                   sections=[
                     self.get_section("__passport_details__"),
                     self.get_section("applicant_details"),
                     self.get_section("address_details"),
                     self.get_section("family_details"),
                     self.get_section("visa_details"),
                     self.get_section("previous_visa_details"),
                     self.get_section("visited_countries"),
                     self.get_section("saarc_country_visits"),
                     self.get_section("reference_details_home"),
                     self.get_section("reference_details_ind"),
                 ]),
        ]

    def get_choice(self, id_: str) -> Choice:
        return next(filter(lambda e: e.id == id_, self._choices))

    def get_field(self, id_: str) -> Field:
        return next(filter(lambda e: e.id == id_, self._fields))

    def get_section(self, id_: str) -> Section | Repeater:
        return next(filter(lambda e: e.id == id_, self._sections))

    def get_survey(self, id_: str) -> Survey:
        return next(filter(lambda e: e.id == id_, self._surveys))

    @staticmethod
    def format_and_validate_input(field: Field, text: str) -> str:
        value = text.strip()
        match field.type:
            case FieldType.DATE:
                date_value = validate_date_input(field, value)
                value = str(date_value)
            case FieldType.CHOICE:
                choice_value = validate_choice_input(field, value)
                value = str(choice_value)
            case _:
                value = format_value(value, field.formatter)
                validators = field.validators or []
                apply_validators(value, validators)
        return value
