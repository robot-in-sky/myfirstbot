from collections.abc import Sequence
from datetime import datetime
from typing import Any

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.entities.forms import Field, FieldType
from src.tgbot.views.buttons import ALL

STORE_DATE_FORMAT = "%Y-%m-%d"
RENDER_DATE_FORMAT = "%d.%m.%Y"

EXAMPLE_TEXT = "Пример"
EXAMPLES_TEXT = "Примеры"
CURRENT_VALUE_TEXT = "Текущее значение"

KB_SORTING_MIN_NUMBER = 10


def render_value(field: Field, value: Any) -> str:
    if value is None:
        return "-"

    match field.type:
        case FieldType.DATE:
            try:
                date_ = datetime.strptime(value, STORE_DATE_FORMAT).date()  # noqa: DTZ007
                return date_.strftime(RENDER_DATE_FORMAT)
            except ValueError:
                pass

        case FieldType.CHOICE:
            return field.choice.output.get(value, value)

        case FieldType.STR:
            if field.validators and "phone" in field.validators:
                return f"{value}"
            return f"<code>{value}</code>"

    return f"{value}"


async def show_field_input(field: Field,
                           value: Any = None, *,
                           message: Message,
                           replace: bool = False) -> Message:
    text = field.input_text

    if field.examples:
        if len(field.examples) == 1:
            text += f"\n\n{EXAMPLE_TEXT}: {render_value(field, field.examples[0])}"
        elif len(field.examples) > 1:
            examples_output = "\n".join([f"• {render_value(field, e)}" for e in field.examples])
            text += f"\n\n{EXAMPLES_TEXT}:\n{examples_output}"

    if value is not None:
        output_value = render_value(field, value)
        text += f"\n\n{CURRENT_VALUE_TEXT}: {output_value}"

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
