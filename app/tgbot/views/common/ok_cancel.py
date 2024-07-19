from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.tgbot.buttons import CANCEL, OK


def ok_cancel_kb(ok_cb: CallbackData, cancel_cb: CallbackData) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=CANCEL, callback_data=cancel_cb.pack()),
                 InlineKeyboardButton(text=OK, callback_data=ok_cb.pack())]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
