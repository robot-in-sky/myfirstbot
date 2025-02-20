from collections.abc import Sequence
from datetime import datetime
from typing import Any

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.entities.form import Field, FieldType
from src.tgbot.views.buttons import ALL, NO, YES
from src.tgbot.views.const import DATE_TIME_FORMAT

CURRENT_VALUE_TEXT = "Текущее значение"
KB_SORTING_MIN_NUMBER = 10


def render_value(field: Field, value: Any) -> str:
    if value is None:
        return "-"
    if field.type == FieldType.DATE:
        try:
            date_ = datetime.strptime(value, "%Y-%m-%d").date()  # noqa: DTZ007
            return date_.strftime(DATE_TIME_FORMAT)
        except ValueError:
            pass
    elif field.type == FieldType.CHOICE:
        return field.choice.output.get(value, value)
    return str(value)


async def show_field_condition(field: Field,
                               message: Message, *,
                               replace: bool = False) -> Message:
    if field.condition_text:  # noqa: SIM108
        text = field.condition_text
    else:
        text = f"{field.name}?"
    keyboard = field_condition_kb()
    if replace:
        await message.delete()
    return await message.answer(text, reply_markup=keyboard)


def field_condition_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=YES),
                                          KeyboardButton(text=NO)]], resize_keyboard=True)


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
        values = choice.all if all_opts else choice.featured
        options = [render_value(field, v) for v in values]
        if len(options) > KB_SORTING_MIN_NUMBER:
            options.sort()
        if not all_opts and len(choice.featured) < len(choice.all):
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
