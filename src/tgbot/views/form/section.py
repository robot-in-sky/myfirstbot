from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from src.entities.form.form import Section
from src.tgbot.views import buttons

from .field import render_value

CHECK_SECTION_TEXT = "Проверьте данные"
SECTION_COMPLETED_TEXT = "✅ Принято"
SELECT_SECTION_FIELD_TEXT = "Какое поле хотите изменить?"


async def show_section(section: Section, data: dict[str, Any], *, message: Message) -> Message:
    text = section_summary(section, data)
    keyboard = section_kb()
    await message.answer(CHECK_SECTION_TEXT, reply_markup=ReplyKeyboardRemove())
    return await message.answer(text, reply_markup=keyboard)


async def show_section_completed(message: Message) -> Message:
    return await message.answer(SECTION_COMPLETED_TEXT, reply_markup=ReplyKeyboardRemove())


def section_summary(section: Section, data: dict[str, Any]) -> str:
    lines = []
    for field in section.fields:
        value = data.get(field.id, None)
        output_value = render_value(field, value) if value is not None else "-"
        line = f"<b>{field.name}</b>: {output_value}"
        lines.append(line)
    lines.append("")
    return "\n".join(lines)


def section_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.EDIT, callback_data="section:edit"),
         InlineKeyboardButton(text=buttons.CONFIRM, callback_data="section:confirm")]])


async def show_section_fields(section: Section, *, message: Message) -> Message:
    text = SELECT_SECTION_FIELD_TEXT
    keyboard = section_fields_kb(section)
    await message.edit_text(text, reply_markup=keyboard)
    return message


def section_fields_kb(section: Section, col: int = 2) -> InlineKeyboardMarkup:
    fields = section.fields
    keyboard = []
    for i in range(0, len(fields), col):
        row = [InlineKeyboardButton(text=f.name, callback_data=f"field:{f.id}")
                    for f in fields[i:i+col]]
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
