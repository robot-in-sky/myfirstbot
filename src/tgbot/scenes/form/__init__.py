from src.tgbot.utils.fields import Field, FormSection

VISA_FIELDS = [
    FormSection(
        id="passport_details",
        name="Паспортные данные",
        fields=[
            Field(
                id="given_name",
                name="Имя",
                input_text="Ваше имя",
                type="text",
                validators={"max_len": 20},
            ),
            Field(
                id="surname",
                name="Имя",
                input_text="Ваша фамилия",
                type="text",
                validators={"max_len": 20},
            ),
        ],
    ),
    FormSection(
        id="address_details",
        name="Данные о месте проживания",
        fields=[
            Field(
                id="country",
                name="Гражданство",
                input_text="Ваше гражданство",
                type="text",
                kb_options={"Россия": "RUS", "Казахстан": "KAZ", "Беларусь": "BLR"},
                kb_columns=3,
                validators={"in": ["Россия", "Казахстан", "Беларусь"]},
            ),
        ],
    ),
    FormSection(
        id="family_details",
        name="Данные о семье",
        fields=[
            Field(
                id="brothers",
                name="Кол-во братьев",
                input_text="Сколько у вас братьев?",
                type="int",
                validators={"min": 0, "max": 20},
            ),
        ],
    ),
]
