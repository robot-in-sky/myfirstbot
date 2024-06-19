from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.user import User
from myfirstbot.tgbot import buttons


def main_menu_kb(user: User) -> ReplyKeyboardMarkup:
    keyboard = [[
            KeyboardButton(text=buttons.NEW_ORDER),
            KeyboardButton(text=buttons.MY_ORDERS),
        ]]

    if user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]:
        keyboard.append([
            KeyboardButton(text=buttons.USERS),
            KeyboardButton(text=buttons.ORDERS),
        ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
