from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.entities.choices import UserRole
from app.entities.query import CountResultItem, QueryResult
from app.entities.user import User
from app.tgbot.buttons import (
    BACK,
    FILTER,
    FILTER_CHECKED,
    FILTER_CHECKMARK,
    PAGE_NEXT,
    PAGE_PREV,
    SEARCH,
    SEARCH_RESET,
    TO_MENU,
)
from app.tgbot.callbacks import (
    UserCallbackData,
    UserFilterCallbackData,
    UserSearchCallbackData,
    UsersCallbackData,
)
from app.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from app.tgbot.utils.helpers import cut_string
from app.tgbot.views.user.user import user_role


async def show_user_filter(
        count_by_role: Sequence[CountResultItem[UserRole]],
        total_count: int,
        callback_data: UserFilterCallbackData,
        *,
        message: Message,
        replace_text: bool = False,
) -> Message:
    params = callback_data.model_dump(exclude_none=True, exclude={"role"})
    params_back = callback_data.model_dump(exclude_none=True)
    keyboard = []
    if len(count_by_role) > 1:
        for item in count_by_role:
            check_mark = FILTER_CHECKMARK if item.value == callback_data.role else ""
            keyboard += [[InlineKeyboardButton(
                            text=f"{check_mark}  {user_role(item.value)} ({item.count})",
                            callback_data=UsersCallbackData(role=item.value, **params).pack(),
                        )]]
    keyboard += [[InlineKeyboardButton(
                    text=BACK,
                    callback_data=UsersCallbackData(**params_back).pack()),
                  InlineKeyboardButton(
                    text=f"Все ({total_count})",
                    callback_data=UsersCallbackData(**params).pack())]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = "Пользователи\n"
    if callback_data.s:
        text += f"Поиск: {callback_data.s}\n"
    text += "Фильтр: выберите роль"
    if replace_text:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(
        text, reply_markup=reply_markup)


async def show_users(
        result: QueryResult,
        callback_data: UsersCallbackData,
        *,
        message: Message,
        replace_text: bool = False,
) -> Message:
    reply_markup = users_result_kb(result, callback_data)
    text = "Пользователи\n"
    if len(result.items) > 0:
        if callback_data.s:
            text += f"Поиск: {callback_data.s}\n"
        if callback_data.role:
            text += f"Фильтр: {user_role(callback_data.role)}\n"
        if replace_text:
            await message.edit_text(text, reply_markup=reply_markup)
            return message
        return await message.answer(text, reply_markup=reply_markup)
    text += "Результатов не найдено"
    return await message.answer(text, reply_markup=reply_markup)


def users_result_kb(
        result: QueryResult[User],
        callback_data: UsersCallbackData,
) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=user_item_text(user),
            callback_data=UserCallbackData(id=user.id).pack(),
        )] for user in result.items]
    keyboard.append(pagination_buttons(result, callback_data))
    keyboard.append(footer_buttons(callback_data))
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


def pagination_buttons(
        result: QueryResult,
        callback_data: UsersCallbackData,
) -> list[InlineKeyboardButton]:
    if result.page is not None and result.total_pages > 1:
        params = callback_data.model_dump(exclude={"page"})
        prev_page = result.page - 1 if result.page > 1 else result.total_pages
        next_page =result.page + 1 if result.page < result.total_pages else 1
        prev_cb = UsersCallbackData(page=prev_page, **params).pack()
        next_cb = UsersCallbackData(page=next_page, **params).pack()
        page_info = f"{result.page}/{result.total_pages}"
        return [InlineKeyboardButton(text=PAGE_PREV, callback_data=prev_cb),
                InlineKeyboardButton(text=page_info, callback_data="_"),
                InlineKeyboardButton(text=PAGE_NEXT, callback_data=next_cb)]
    return []


def footer_buttons(callback_data: UsersCallbackData) -> list[InlineKeyboardButton]:
    keyboard = [InlineKeyboardButton(text=TO_MENU, callback_data="to_menu")]

    params = callback_data.model_dump(exclude={"page"})
    filter_cb = UserFilterCallbackData(**params).pack()
    filter_text = FILTER if callback_data.role is None else FILTER_CHECKED
    keyboard += [InlineKeyboardButton(text=filter_text, callback_data=filter_cb)]

    if callback_data.s is None:
        search_cb = UserSearchCallbackData(**params).pack()
        search_text = SEARCH
    else:
        _params = callback_data.model_dump(exclude={"page", "s"})
        search_cb = UsersCallbackData(**_params).pack()
        search_text = SEARCH_RESET
    keyboard += [InlineKeyboardButton(text=search_text, callback_data=search_cb)]

    return keyboard