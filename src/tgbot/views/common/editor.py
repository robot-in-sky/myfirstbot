from collections.abc import Sequence
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.tgbot import buttons
from src.tgbot.callbacks import EditorCallbackData
from src.tgbot.utils.fields import Field


def editor_summary(
        fields: Sequence[Field],
        data: dict[str, Any],
        selected: str | None = None) -> str:
    lines = ["<b>Страница 1/1</b>", ""]
    for field in fields:
        value = data.get(field.id, "-")
        line = f"    <b>{field.name}</b>: {value}    "
        if selected and field.id == selected:
            line = f"    <b>{field.name}</b>: <u>{value} </u> {buttons.EDITOR_EDIT}    "
        lines.append(line)
    lines.append("")
    lines.append("<i>Отредактируйте значения полей</i>")
    lines.append("<i>Используйте кнопки вверх/вниз</i>")
    return "\n".join(lines)


def editor_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.PAGE_PREV, callback_data="_"),
         InlineKeyboardButton(text=buttons.EDITOR_UP, callback_data=EditorCallbackData(action="up").pack()),
         InlineKeyboardButton(text=buttons.PAGE_NEXT, callback_data="_")],
        [InlineKeyboardButton(text=buttons.EDITOR_RESET, callback_data=EditorCallbackData(action="return").pack()),
         InlineKeyboardButton(text=buttons.EDITOR_DOWN, callback_data=EditorCallbackData(action="down").pack()),
         InlineKeyboardButton(text=buttons.EDITOR_EDIT, callback_data=EditorCallbackData(action="edit").pack())],
        [InlineKeyboardButton(text=buttons.CANCEL, callback_data=EditorCallbackData(action="cancel").pack()),
         InlineKeyboardButton(text=buttons.SAVE, callback_data=EditorCallbackData(action="save").pack())]])
