from collections.abc import Sequence
from typing import Any

from aiogram.types import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from myfirstbot.tgbot.buttons import CANCEL, SAVE
from myfirstbot.tgbot.editors.base.field import Field


def editor_kb(target: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="▲", callback_data="field:prev"),
            InlineKeyboardButton(text="▼", callback_data="field:next"),
            InlineKeyboardButton(text="✏️", callback_data="field:edit")
        ],
        [
            InlineKeyboardButton(text=SAVE, callback_data=f"{target}:save")
        ],
        [
            InlineKeyboardButton(text=CANCEL, callback_data=f"{target}:cancel")
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
