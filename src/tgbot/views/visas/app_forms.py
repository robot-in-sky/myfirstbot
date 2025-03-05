from collections.abc import Sequence
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.base import QueryCountItem, QueryResult
from src.entities.users import User
from src.entities.visas import AppForm, AppFormStatus
from src.tgbot.views.buttons import BACK, FILTER_CHECKMARK
from src.tgbot.views.const import COLUMN_DELIMITER
from src.tgbot.views.keyboards import filter_buttons, pagination_buttons
from src.tgbot.views.users.user import is_admin

from .app_form import app_form_status


async def show_app_forms(  # noqa: PLR0913
        result: QueryResult[AppForm], *,
        status: AppFormStatus | None = None,
        search: str | None = None,
        user_id: UUID | None = None,
        message: Message,
        replace: bool = False,
        current_user: User,
) -> Message:
    reply_markup = app_form_result_kb(result,
                                      filter_=bool(status),
                                      search=bool(search))
    text = get_app_forms_title(user_id, current_user) + "\n"
    if len(result.items) > 0:
        if search:
            text += f"Поиск: {search}\n"
        if status:
            text += f"Фильтр: {app_form_status(status)}\n"
        if replace:
            await message.edit_text(text, reply_markup=reply_markup)
            return message
        return await message.answer(text, reply_markup=reply_markup)
    text += "Результатов не найдено"
    return await message.answer(text, reply_markup=reply_markup)


def get_app_forms_title(user_id: int | None, current_user: User) -> str:
    if user_id:
        if user_id == current_user.id:
            return "Мои заказы"
        return f"Заказы пользователя {user_id}"
    return "Заказы"


def app_form_result_kb(
        result: QueryResult[AppForm], *,
        filter_: bool = False, search: bool = False) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(
                    text=app_form_item_text(user),
                    callback_data=f"app_form:{user.id}",
                        )] for user in result.items]
    keyboard.append(pagination_buttons(result))
    keyboard.append(filter_buttons(filter_=filter_, search=search))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def app_form_item_text(app_form: AppForm, current_user: User) -> str:
    columns = []
    if is_admin(current_user):
        columns.append(str(app_form.user_id))
    columns.append(app_form.country)
    if app_form.data:
        given_name = app_form.data.get("passport_details.given_name")
        surname = app_form.data.get("passport_details.surname")
        if given_name and surname:
            short_name = f"{given_name} {surname[0]}."
            columns.append(short_name)
    columns.append(app_form.status)
    return COLUMN_DELIMITER.join(columns)


async def show_app_form_filter(  # noqa: PLR0913
        count_by_status: Sequence[QueryCountItem[AppFormStatus]], *,
        total_count: int,
        status: AppFormStatus | None = None,
        search: str | None = None,
        user_id: UUID | None = None,
        message: Message,
        replace: bool = False,
        current_user: User,
) -> Message:
    keyboard = []
    for item in count_by_status:
        check_mark = FILTER_CHECKMARK if item.value == status else ""
        keyboard += [[InlineKeyboardButton(
            text=f"{check_mark}  {app_form_status(item.value)} ({item.count})",
            callback_data=f"status:{item}")]]
    keyboard += [[InlineKeyboardButton(text=BACK, callback_data="back"),
                  InlineKeyboardButton(text=f"Все ({total_count})", callback_data="status:all")]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = get_app_forms_title(user_id, current_user) + "\n"
    if search:
        text += f"Поиск: {search}\n"
    text += "Фильтр: выберите статус"
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(
        text, reply_markup=reply_markup)
