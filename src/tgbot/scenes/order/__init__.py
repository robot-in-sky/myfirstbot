from src.tgbot.utils.fields import Field

ORDER_FIELDS = [
    Field(
        id="label",
        name="Надпись",
        input_text="Какую бы Вы хотели надпись? Введите текст",
        type="text",
        validators={"max_len": 20},
    ),
    Field(
        id="size",
        name="Размер",
        input_text="Введите размер",
        type="int",
        kb_options={"42": 42, "46": 46, "48": 48},
        kb_columns=3,
        validators={"in": [42, 46, 48]},
    ),
    Field(
        id="qty",
        name="Количество",
        input_text="Введите количество",
        type="int",
        validators={"min": 1, "max": 10},
    ),
]
