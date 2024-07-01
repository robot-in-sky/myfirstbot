from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.query import QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.callbacks import UserCallbackData, UsersCallbackData
from myfirstbot.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from myfirstbot.tgbot.utils.helpers import cut_string
from myfirstbot.tgbot.views.common.pagination import pagination_buttons
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.user.user import user_role


async def show_users(
        result: QueryResult,
        callback_data: UsersCallbackData,
        *,
        current_user: User,
        message: Message,
) -> Message:
    if len(result.items) > 0:
        text = "Пользователи\n"
        if callback_data.role:
            text += f"Роль: {user_role(callback_data.role)}"
        keyboard = users_result_kb(result, callback_data)
        return await message.answer(text, reply_markup=keyboard)
    return await message.answer("У Вас ещё нет заказов",
                                reply_markup=main_menu_kb(current_user))


def users_result_kb(
        result: QueryResult[User],
        callback_data: UsersCallbackData,
) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=user_item_text(user),
            callback_data=UserCallbackData(id=user.id).pack(),
        )] for user in result.items]
    if result.total_pages and result.total_pages > 1:
        keyboard.append(pagination_buttons(result, callback_data))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def user_item_text(user: User) -> str:
    columns = [
        str(user.id),
        user.user_name,
        user.first_name or "",
        user_role(user.role),
    ]
    text = COLUMN_DELIMITER.join(columns)
    return cut_string(text, BUTTON_TEXT_MAX_LEN)
