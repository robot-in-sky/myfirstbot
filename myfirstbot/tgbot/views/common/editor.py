from collections.abc import Sequence
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from myfirstbot.tgbot.buttons import CANCEL, EDITOR_DOWN, EDITOR_EDIT, EDITOR_UP, SAVE
from myfirstbot.tgbot.callbacks import EditorCallbackData
from myfirstbot.tgbot.utils.fields import Field


def editor_summary(
        fields: Sequence[Field],
        data: dict[str, Any],
        selected: str | None = None) -> str:
    lines = []
    for field in fields:
        value = data.get(field.id, "-")
        line = f"<b>{field.name}</b>: {value}"
        if selected and field.id == selected:
            line = f"<b>{field.name}</b>: <u>{value} </u> {EDITOR_EDIT}"
        lines.append(line)
    lines.append("")
    lines.append("<i>Отредактируйте значения полей</i>")
    lines.append("<i>Используйте кнопки вверх/вниз</i>")
    return "\n".join(lines)


def editor_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=EDITOR_UP, callback_data=EditorCallbackData(action="up").pack()),
         InlineKeyboardButton(text=EDITOR_DOWN, callback_data=EditorCallbackData(action="down").pack()),
         InlineKeyboardButton(text=EDITOR_EDIT, callback_data=EditorCallbackData(action="edit").pack())],

        [InlineKeyboardButton(text=SAVE, callback_data=EditorCallbackData(action="save").pack())],
        [InlineKeyboardButton(text=CANCEL, callback_data=EditorCallbackData(action="cancel").pack())]])
