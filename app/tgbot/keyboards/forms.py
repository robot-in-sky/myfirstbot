from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заполнить анкету'),
            KeyboardButton(text='Мои анкеты'),
        ],
        [
            KeyboardButton(text='Аккаунт'),
        ],
    ],
    resize_keyboard=True
)
