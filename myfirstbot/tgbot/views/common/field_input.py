from collections.abc import Sequence
from typing import Any

from aiogram.types import ForceReply, KeyboardButton, Message, ReplyKeyboardMarkup

from myfirstbot.tgbot.utils.fields import Field


async def show_field_input(field: Field, value: Any = None, *, message: Message) -> Message:
    return await message.answer(
        field.input_text,
        reply_markup=field_input_kb(field, value)
    )

def field_input_kb(field: Field, value: Any = None) -> ReplyKeyboardMarkup | ForceReply:
    if field.kb_options:
        return field_options_kb([*field.kb_options.keys()], field.kb_columns)
    placeholder = str(value) or field.placeholder or None
    return ForceReply(
        force_reply=True,
        input_field_placeholder=placeholder
    )

def field_options_kb(options: Sequence[Any], col: int = 2) -> ReplyKeyboardMarkup:
    keyboard = []
    for i in range(0, len(options), col):
        row = [KeyboardButton(text=opt) for opt in options[i:i+col]]
        keyboard.append(row)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
