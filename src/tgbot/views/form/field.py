from collections.abc import Sequence
from typing import Any

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.tgbot.utils.fields import Field

CURRENT_VALUE_TEXT = "Текущее значение"

async def show_field_input(field: Field, value: Any = None, *, message: Message) -> Message:
    text = field.input_text
    if value is not None:
        text += f"\n{CURRENT_VALUE_TEXT}: {value}"
    return await message.answer(text, reply_markup=field_input_kb(field))


def field_input_kb(field: Field) -> ReplyKeyboardMarkup:
    options = []
    if field.kb_options:
        options = [*field.kb_options.keys()]
    kwargs = {}
    if field.kb_columns:
        kwargs["col"] = field.kb_columns
    return options_kb(options, **kwargs)


def options_kb(options: Sequence[Any], col: int = 2) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
    if len(options) == 0:
        return ReplyKeyboardRemove()
    keyboard = []
    for i in range(0, len(options), col):
        row = [KeyboardButton(text=opt) for opt in options[i:i+col]]
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
