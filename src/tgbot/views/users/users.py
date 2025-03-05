from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.base import QueryCountItem, QueryResult
from src.entities.users import User, UserRole
from src.tgbot.utils.helpers import cut_string
from src.tgbot.views.buttons import BACK, FILTER_CHECKMARK
from src.tgbot.views.const import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from src.tgbot.views.keyboards import filter_buttons, pagination_buttons

from .user import user_role


async def show_users(
        result: QueryResult[User], *,
        role: UserRole | None = None,
        search: str | None = None,
        message: Message,
        replace: bool = False,
) -> Message:
    reply_markup = users_result_kb(result,
                                   filter_=bool(role),
                                   search=bool(search))
    text = "Пользователи\n"
    if len(result.items) > 0:
        if search:
            text += f"Поиск: {search}\n"
        if role:
            text += f"Фильтр: {user_role(role)}\n"
        if replace:
            await message.edit_text(text, reply_markup=reply_markup)
            return message
        return await message.answer(text, reply_markup=reply_markup)
    text += "Результатов не найдено"
    return await message.answer(text, reply_markup=reply_markup)


def users_result_kb(
        result: QueryResult[User], *,
        filter_: bool = False, search: bool = False) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(
                    text=user_item_text(user),
                    callback_data=f"user:{user.id}",
                        )] for user in result.items]
    keyboard.append(pagination_buttons(result))
    keyboard.append(filter_buttons(filter_=filter_, search=search))
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


async def show_user_filter(  # noqa: PLR0913
        count_by_role: Sequence[QueryCountItem[UserRole]], *,
        total_count: int,
        role: UserRole | None = None,
        search: str | None = None,
        message: Message,
        replace: bool = False,
) -> Message:
    keyboard = []
    for item in count_by_role:
        check_mark = FILTER_CHECKMARK if item.value == role else ""
        keyboard += [[InlineKeyboardButton(
                        text=f"{check_mark}  {user_role(item.value)} ({item.count})",
                        callback_data=f"role:{item}")]]
    keyboard += [[InlineKeyboardButton(text=BACK, callback_data="back"),
                  InlineKeyboardButton(text=f"Все ({total_count})", callback_data="role:all")]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = "Пользователи\n"
    if search:
        text += f"Поиск: {search}\n"
    text += "Фильтр: выберите роль"
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(
        text, reply_markup=reply_markup)
