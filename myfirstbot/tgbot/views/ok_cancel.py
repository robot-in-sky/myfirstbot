from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from myfirstbot.tgbot.buttons import CANCEL, OK


def ok_cancel_kb(target: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=OK, callback_data=f"{target}:ok"),
         InlineKeyboardButton(text=CANCEL, callback_data=f"{target}:cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
