from collections.abc import Sequence
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from myfirstbot.exceptions import ValidationError

from .field import Field
from .keyboards import editor_kb, field_input_kb


class Editor:
    def __init__(
            self,
            fields: Sequence[Field],
            save_cancel_target: str,
    ) -> None:
        self.fields = {f.id: f for f in fields}
        self.save_cancel_target = save_cancel_target

    @property
    def field_ids(self) -> list[str]:
        return [*self.fields.keys()]

    def summary(self, data: dict[str, Any], selected: str | None = None) -> str:
        lines = []
        for field in self.fields.values():
            value = data.get(field.id, "-")
            line = f"<b>{field.name}</b>: {value}"
            if selected is None:
                line = f"{line}"
            elif field.id == selected:
                line = f"[ {line} ] ✏️"
            else:
                line = f"  {line}"
            lines.append(line)
        return "\n".join(lines)

    async def show_editor(self, field_id: str, state: FSMContext, message: Message) -> None:
        data = await state.get_data()
        _message = await message.answer(
            self.summary(data, field_id),
            reply_markup=editor_kb(self.save_cancel_target),
        )
        if editor_id := data.get("_editor_id"):
            await message.chat.delete_message(editor_id)
        await state.update_data({"_editor_id": _message.message_id})

    async def refresh_editor(self, field_id: str, state: FSMContext, message: Message) -> None:
        data = await state.get_data()
        _message = await message.edit_text(
            self.summary(data, field_id),
            reply_markup=editor_kb(self.save_cancel_target),
        )
        await state.update_data({"_editor_id": _message.message_id})

    async def show_input(self, field_id: str, message: Message) -> None:
        if f := self.fields.get(field_id, None):
            await message.answer(f.text, reply_markup=field_input_kb(f))

    async def validate_input(self, field_id: str, state: FSMContext, message: Message) -> None:
        if f := self.fields.get(field_id, None):
            value = message.text

            match f.type:
                case "text":
                    if f.validators.get("limit", None) and len(value) > f.validators["limit"]:
                        err_msg = f"Длина не более {f.validators["limit"]} символов."
                        raise ValidationError(err_msg)

                case "int":
                    try:
                        value = int(value)
                    except (TypeError, ValueError):
                        err_msg = "Неверный формат."
                        raise ValidationError(err_msg) from None

                    if f.validators.get("min", None) and value < f.validators["min"]:
                        err_msg = f"Минимальное значение {f.validators["min"]}."
                        raise ValidationError(err_msg)

                    if f.validators.get("max", None) and value > f.validators["max"]:
                        err_msg = f"Макисмальное значение {f.validators["max"]}."
                        raise ValidationError(err_msg)

            if f.validators.get("in", None) and value not in f.validators["in"]:
                err_msg = f"Допустимые значения {f.validators["in"]}."
                raise ValidationError(err_msg)

            await state.update_data({field_id: value})
