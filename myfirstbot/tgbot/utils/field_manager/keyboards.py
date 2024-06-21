from collections.abc import Sequence
from typing import Any

from aiogram.types import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from myfirstbot.tgbot.buttons import CANCEL, EDITOR_DOWN, EDITOR_EDIT, EDITOR_UP, SAVE
from myfirstbot.tgbot.utils.field_manager.field import Field


def editor_kb() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text=EDITOR_UP, callback_data="editor_up"),
            InlineKeyboardButton(text=EDITOR_DOWN, callback_data="editor_down"),
            InlineKeyboardButton(text=EDITOR_EDIT, callback_data="editor_edit")
        ],
        [
            InlineKeyboardButton(text=SAVE, callback_data="editor_save")
        ],
        [
            InlineKeyboardButton(text=CANCEL, callback_data="editor_cancel")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def field_options_kb(options: Sequence[Any], col: int = 2) -> ReplyKeyboardMarkup:
    keyboard = []
    for i in range(0, len(options), col):
        row = [KeyboardButton(text=opt) for opt in options[i:i+col]]
        keyboard.append(row)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def field_input_kb(field: Field) -> ReplyKeyboardMarkup | ForceReply:
    if field.keyboard:
        return field_options_kb([*field.keyboard.keys()], field.kb_columns)
    return ForceReply(
        force_reply=True,
        input_field_placeholder=field.placeholder if field.placeholder else None
    )
