from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заполнить анкету"),
            KeyboardButton(text="Мои анкеты"),
        ],
        [
            KeyboardButton(text="Аккаунт"),
        ],
    ],
    resize_keyboard=True,
)
