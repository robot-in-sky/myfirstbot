from collections.abc import Sequence
from typing import Any

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.entities.form import Field
from src.tgbot.views.buttons import ALL

CURRENT_VALUE_TEXT = "Текущее значение"
KB_SORTING_MIN_NUMBER = 10


def render_value(field: Field, value: Any) -> str:
    if field.choice is not None:
        return field.choice.output.get(value, value)
    return str(value)


async def show_field_input(field: Field,
                           value: Any = None, *,
                           message: Message,
                           replace: bool = False) -> Message:
    text = field.input_text
    if value is not None:
        output_value = render_value(field, value)
        text += f"\n{CURRENT_VALUE_TEXT}: {output_value}"
    keyboard = field_input_kb(field)
    if replace:
        await message.delete()
    return await message.answer(text, reply_markup=keyboard)


async def show_all_options(field: Field, message: Message) -> Message:
    keyboard = field_input_kb(field, all_opts=True)
    await message.delete()
    return await message.answer(ALL, reply_markup=keyboard)


def field_input_kb(field: Field, *, all_opts: bool = False) -> ReplyKeyboardMarkup:
    options = []
    if field.choice:
        choice = field.choice
        values = choice.all if all_opts else choice.default
        options = [render_value(field, v) for v in values]
        if len(options) > KB_SORTING_MIN_NUMBER:
            options.sort()
        if not all_opts and len(choice.default) < len(choice.all):
            options.append(ALL)
    return options_kb(options)


def options_kb(options: Sequence[Any], col: int = 2) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
    if len(options) == 0:
        return ReplyKeyboardRemove()
    keyboard = []
    for i in range(0, len(options), col):
        row = [KeyboardButton(text=opt) for opt in options[i:i+col]]
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
