from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.query import QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.buttons import PAGE_NEXT, PAGE_PREV
from myfirstbot.tgbot.callbacks import UsersCallbackData
from myfirstbot.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from myfirstbot.tgbot.utils.helpers import cut_string
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
        keyboard = users_result_kb(result, callback_data)
        if callback_data.page:
            await message.edit_reply_markup(reply_markup=keyboard)
            return message
        lines = ["Пользователи"]
        if callback_data.role:
            lines.append(f"Роль: {user_role(callback_data.role)}")
        text = "\n".join(lines)
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
            callback_data=f"user:get:{user.id}",
        )] for user in result.items]
    if result.total_pages > 1:
        keyboard.append(pagination_buttons(result, callback_data))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def user_item_text(user: User) -> str:
    columns = [
        str(user.id),
        user.user_name,
        user.first_name,
        user_role(user.role),
    ]
    text = COLUMN_DELIMITER.join(columns)
    return cut_string(text, BUTTON_TEXT_MAX_LEN)


def pagination_buttons(
        result: QueryResult,
        callback_data: UsersCallbackData,
) -> list[InlineKeyboardButton]:
    callback_page = callback_data.page
    callback_data.page = result.page - 1 if result.page > 1 else result.total_pages
    callback_prev = callback_data.pack()
    callback_data.page = result.page + 1 if result.page < result.total_pages else 1
    callback_next = callback_data.pack()
    callback_data.page = callback_page
    page_info = f"{result.page}/{result.total_pages}"
    return [InlineKeyboardButton(text=PAGE_PREV, callback_data=callback_prev),
            InlineKeyboardButton(text=page_info, callback_data="_"),
            InlineKeyboardButton(text=PAGE_NEXT, callback_data=callback_next)]
