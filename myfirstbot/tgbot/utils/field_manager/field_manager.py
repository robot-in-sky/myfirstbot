from collections.abc import Sequence
from typing import Any

from aiogram.types import Message

from myfirstbot.exceptions import ValidationError
from myfirstbot.tgbot.buttons import EDITOR_EDIT

from .field import Field
from .keyboards import editor_kb, field_input_kb


class FieldManager:
    def __init__(
            self,
            fields: Sequence[Field],
    ) -> None:
        self.fields = {f.id: f for f in fields}

    @property
    def ids(self) -> list[str]:
        return [*self.fields.keys()]

    def id_by_index(self, index: int) -> str | None:
        try:
            return self.ids[index]
        except IndexError:
            return None

    def index_by_id(self, id_: str) -> int | None:
        try:
            return self.ids.index(id_)
        except ValueError:
            return None

    def summary(self, data: dict[str, Any], selected: str | None = None) -> str:
        lines = []
        for field in self.fields.values():
            value = data.get(field.id, "-")
            line = f"<b>{field.name}</b>: {value}"
            if selected:
                if field.id == selected:  # noqa: SIM108
                    line = f"[ {line} ] {EDITOR_EDIT}"
                else:
                    line = f"  {line}"
            lines.append(line)
        return "\n".join(lines)

    async def show_editor(
            self,
            data: dict[str, Any],
            selected: str,
            *,
            message: Message,
            replace_text: bool = False,
    ) -> Message:
        text = self.summary(data, selected)
        markup = editor_kb()
        if replace_text:
            return await message.edit_text(text, reply_markup=markup)
        return await message.answer(text, reply_markup=markup)

    async def show_input(self, id_: str, message: Message) -> Message | None:
        if f := self.fields.get(id_, None):
            return await message.answer(f.text, reply_markup=field_input_kb(f))
        return None

    async def validate_input(self, id_: str, text: str) -> None:
        if f := self.fields.get(id_, None):
            match f.type:
                case "text":
                    if f.validators.get("limit", None) and len(text) > f.validators["limit"]:
                        err_msg = f"Длина не более {f.validators["limit"]} символов."
                        raise ValidationError(err_msg)

                case "int":
                    try:
                        text = int(text)
                    except (TypeError, ValueError):
                        err_msg = "Неверный формат."
                        raise ValidationError(err_msg) from None

                    if f.validators.get("min", None) and text < f.validators["min"]:
                        err_msg = f"Минимальное значение {f.validators["min"]}."
                        raise ValidationError(err_msg)

                    if f.validators.get("max", None) and text > f.validators["max"]:
                        err_msg = f"Макисмальное значение {f.validators["max"]}."
                        raise ValidationError(err_msg)

            if f.validators.get("in", None) and text not in f.validators["in"]:
                err_msg = f"Допустимые значения {f.validators["in"]}."
                raise ValidationError(err_msg)
