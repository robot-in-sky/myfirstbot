from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.forms import Section
from src.tgbot.views import buttons

CHECK_SECTION_DATA_TEXT = "Проверьте внимательно все данные"
SELECT_SECTION_FIELD_TEXT = "Какое поле хотите изменить?"


async def show_section(
        section: Section,
        data: dict[str, Any], *,
        message: Message,
        replace: bool = False,
) -> Message:
    text = CHECK_SECTION_DATA_TEXT
    text += f"\n<b>{section.name}</b>\n\n"
    text += section_summary(section, data)
    keyboard = section_kb()
    if replace:
        await message.edit_text(text, reply_markup=keyboard)
        return message
    return await message.answer(text, reply_markup=keyboard)


def section_summary(section: Section, data: dict[str, Any]) -> str:
    lines = []
    for field in section.fields:
        value = data.get(field.id, "-")
        line = f"<b>{field.name}</b>: {value}"
        lines.append(line)
    lines.append("")
    return "\n".join(lines)


def section_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.CANCEL, callback_data="section:cancel"),
         InlineKeyboardButton(text=buttons.EDIT, callback_data="section:edit"),
         InlineKeyboardButton(text=buttons.CONFIRM, callback_data="section:confirm")]])


async def show_section_fields(
        section: Section, *,
        message: Message,
        replace: bool = False,
) -> Message:
    text = SELECT_SECTION_FIELD_TEXT
    keyboard = section_fields_kb(section)
    if replace:
        await message.edit_text(text, reply_markup=keyboard)
        return message
    return await message.answer(text, reply_markup=keyboard)


def section_fields_kb(section: Section, col: int = 2) -> InlineKeyboardMarkup:
    fields = section.fields
    keyboard = []
    for i in range(0, len(fields), col):
        row = [InlineKeyboardButton(text=f.name) for f in fields[i:i+col]]
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
