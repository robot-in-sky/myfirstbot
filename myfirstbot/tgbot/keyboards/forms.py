from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать заказ"),
            KeyboardButton(text="Мои заказы"),
        ],
        [
            KeyboardButton(text="Аккаунт"),
        ],
    ],
    resize_keyboard=True,
)
