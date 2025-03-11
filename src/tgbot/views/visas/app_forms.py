from collections.abc import Sequence
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.base import QueryCountItem, QueryResult
from src.entities.users import User
from src.entities.visas import AppForm, AppFormStatus
from src.tgbot.views.buttons import BACK, FILTER_CHECKMARK
from src.tgbot.views.const import COLUMN_DELIMITER
from src.tgbot.views.keyboards import bottom_buttons, pagination_buttons
from src.tgbot.views.users.user import is_admin

from .app_form import app_form_status, app_form_applicant_data
from .visa_app import visa_country


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
                                      current_user=current_user,
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


def app_form_result_kb(result: QueryResult[AppForm], *,
                       current_user: User,
                       filter_: bool = False,
                       search: bool = False) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(
                    text=app_form_item_text(app_form, current_user=current_user),
                    callback_data=f"app_form:{app_form.id}",
                        )] for app_form in result.items]
    keyboard.append(pagination_buttons(result))
    keyboard.append(bottom_buttons(filter_=filter_, search=search))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def app_form_item_text(app_form: AppForm, *, current_user: User) -> str:
    columns = []
    if is_admin(current_user):
        columns.append(str(app_form.user_id))
    country = visa_country(app_form.country)
    columns.append(country)
    if data := app_form_applicant_data(app_form):
        applicant = f"{data["given_name"]} {data["surname"][0]}."
        # applicant = f"{data["surname"]} {data["given_name"]}"
        columns.append(applicant)
    status = app_form_status(app_form.status)
    columns.append(status)
    return COLUMN_DELIMITER.join(columns)


async def show_app_form_filter(  # noqa: PLR0913
        count_by_status: Sequence[QueryCountItem[AppFormStatus]],
        total_count: int, *,
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
            callback_data=f"filter:status:{item.value}")]]
    keyboard += [[InlineKeyboardButton(text=BACK, callback_data="back"),
                  InlineKeyboardButton(text=f"Все ({total_count})", callback_data="filter:status:all")]]
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
