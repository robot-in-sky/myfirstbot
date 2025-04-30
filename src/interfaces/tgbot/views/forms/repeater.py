from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from core.entities.forms import YesNo
from core.entities.forms.form import Repeater
from interfaces.tgbot.views import buttons

from .field import render_value

CHECK_REPEATER_TEXT = "Проверьте данные"
REPEATER_COMPLETED_TEXT = "✅ Принято"
REPEATER_RESET_TEXT = "Начнём сначала"


async def show_repeater_description(repeater: Repeater, *,
                                    message: Message,
                                    replace: bool = False) -> Message:
    if replace:
        return await message.edit_text(repeater.description)
    return await message.answer(repeater.description)


async def show_repeater(repeater: Repeater, data: list[dict[str, Any]], *, message: Message) -> Message:
    text = repeater_summary(repeater, data)
    show_reset = len(data) > 0
    keyboard = repeater_kb(show_reset=show_reset)
    return await message.answer(text, reply_markup=keyboard)


async def show_repeater_completed(message: Message) -> Message:
    return await message.answer(REPEATER_COMPLETED_TEXT, reply_markup=ReplyKeyboardRemove())


def repeater_summary(repeater: Repeater, data: list[dict[str, Any]]) -> str:
    cond_field = repeater.condition_field
    cond_name_output = f"<b>{cond_field.name}</b>:"
    if not len(data) > 0:
        cond_value_output = render_value(cond_field, YesNo.NO)
        return f"{cond_name_output} {cond_value_output}"

    lines = [cond_name_output, ""]
    for group in data:
        first_field = True
        for field in repeater.repeater_fields:
            if field.hidden:
                continue
            marker = "•" if first_field else " "
            marker = f"<code>{marker}</code>"
            value = group.get(field.id, None)
            value_output = render_value(field, value) if value is not None else "-"
            line = ""
            if len(group) > 1:
                line += f"{marker} <b>{field.name}</b>: {value_output}"
            else:
                line += f"{marker} {value_output}"
            first_field = False
            lines.append(line)
        if len(group) > 1:
            lines.append("")
    return "\n".join(lines)


def repeater_kb(*, show_reset: bool = True) -> InlineKeyboardMarkup:
    kb_row = [InlineKeyboardButton(text=buttons.ADD, callback_data="repeater:add")]
    if show_reset:
        kb_row += [InlineKeyboardButton(text=buttons.RESET, callback_data="repeater:reset")]
    kb_row += [InlineKeyboardButton(text=buttons.CONFIRM, callback_data="repeater:confirm")]
    return InlineKeyboardMarkup(inline_keyboard=[kb_row])
