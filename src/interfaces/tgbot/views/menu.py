from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core.entities.users import User, UserRole
from interfaces.tgbot.views import buttons
from interfaces.tgbot.views.users.user import user_role

MAIN_MENU_TEXT = ("Это тестовая версия визового бота\n\n"
                  "Главное меню")

def signin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=user_role(UserRole.USER), callback_data="signin_as:user"),
            InlineKeyboardButton(text=user_role(UserRole.AGENT), callback_data="signin_as:agent")]])


async def show_menu(*, message: Message,
                    current_user: User,
                    replace: bool = False) -> Message:
    text = MAIN_MENU_TEXT
    reply_markup = main_menu_kb(current_user)
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def main_menu_kb(current_user: User) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=buttons.APPLY_VISA, callback_data="apply_visa")],
                [InlineKeyboardButton(text=buttons.MY_APP_FORMS, callback_data="my_app_forms")]]
    if current_user.role >= UserRole.AGENT:
        keyboard += [[InlineKeyboardButton(text=buttons.USERS, callback_data="manage_users")],
                     [InlineKeyboardButton(text=buttons.MANAGE_APP_FORMS, callback_data="manage_app_forms")]]
        # keyboard = [[keyboard[0][0], keyboard[1][0]],
        #             [keyboard[0][1], keyboard[1][1]]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
