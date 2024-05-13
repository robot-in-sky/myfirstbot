from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CANCEL = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена") ],
    ],
    resize_keyboard=True,
)

CONFIRM_CANCEL = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Подтвердить") ],
        [KeyboardButton(text="❌ Отмена") ],
    ],
    resize_keyboard=True,
)
