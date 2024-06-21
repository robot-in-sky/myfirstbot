from typing import Any

from myfirstbot.tgbot.utils.field_manager import Field, FieldManager


class OrderFieldManager(FieldManager):
    def __init__(self) -> None:
        super().__init__(
            fields=[
                Field(
                    id="label",
                    name="Надпись",
                    text="Какую бы Вы хотели надпись? Введите текст:",
                    placeholder="Надпись",
                    type="text",
                    validators={"limit": 20},
                ),
                Field(
                    id="size",
                    name="Размер",
                    text="Введите размер:",
                    type="int",
                    keyboard={"42": 42, "46": 46, "48": 48},
                    kb_columns=3,
                    validators={"in": [42, 46, 48]},
                ),
                Field(
                    id="qty",
                    name="Количество",
                    text="Введите количество:",
                    placeholder="1",
                    type="int",
                    validators={"min": 1, "max": 10},
                ),
            ],
        )

    def summary(self, data: dict[str, Any], selected: str | None = None) -> str:
        output = f"<b>Заказ #{data["id"]}</b>\n\n"
        output += super().summary(data, selected) + "\n\n"
        output += "<i>Отредактируйте значения полей.</i>\n"
        output += "<i>Используйте кнопки вверх/вниз.</i>\n\n"
        return output


order_fields = OrderFieldManager()
