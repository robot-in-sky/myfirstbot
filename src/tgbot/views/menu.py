from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.choices import UserRole
from src.entities.user import User
from src.tgbot.callbacks import OrdersCallbackData, UsersCallbackData
from src.tgbot.views import buttons
from src.tgbot.views.user.user import user_role


def signin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=user_role(UserRole.USER),
                                 callback_data="signin_as:user"),
            InlineKeyboardButton(text=user_role(UserRole.AGENT),
                                 callback_data="signin_as:agent")]])


async def show_menu(
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:
    text = "Главное меню"
    reply_markup = main_menu_kb(current_user)
    if replace_text:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def main_menu_kb(current_user: User) -> InlineKeyboardMarkup:
    keyboard = [[
            InlineKeyboardButton(
                text=buttons.NEW_ORDER,
                callback_data="new_order"),
            InlineKeyboardButton(
                text=buttons.MY_ORDERS,
                callback_data=OrdersCallbackData(user_id=current_user.id).pack())]]
    if current_user.role >= UserRole.AGENT:
        keyboard += [[InlineKeyboardButton(
            text=buttons.USERS,
            callback_data=UsersCallbackData().pack()),
            InlineKeyboardButton(
                text=buttons.ORDERS,
                callback_data=OrdersCallbackData().pack())]]
        keyboard = [[keyboard[0][0], keyboard[1][0]],
                    [keyboard[0][1], keyboard[1][1]]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
