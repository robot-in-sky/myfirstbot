from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CANCEL_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена") ],
    ],
    resize_keyboard=True,
)
