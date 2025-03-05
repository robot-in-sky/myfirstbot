from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.users import User
from src.entities.visas import AppForm, AppFormStatus
from src.tgbot.views import buttons
from src.tgbot.views.const import DATE_TIME_FORMAT
from src.tgbot.views.users.user import is_admin
from src.tgbot.views.visas.visa_app import visa_summary


async def show_app_form(app_form: AppForm, *,
                        current_user: User,
                        message: Message,
                        replace: bool = False,
                        to_menu: bool = False) -> Message:
    text = app_form_summary(app_form)
    reply_markup = app_form_actions_kb(app_form, current_user=current_user, to_menu=to_menu)
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def app_form_status(status: AppFormStatus) -> str:
    return {
        AppFormStatus.TRASH: "Удалён",
        AppFormStatus.DRAFT: "Черновик",
        AppFormStatus.PENDING: "На проверке",
        AppFormStatus.ACCEPTED: "В работе",
        AppFormStatus.COMPLETED: "Завершён",
    }.get(status, f"{status}")


def app_form_summary(app_form: AppForm) -> str:
    applicant = "-"
    if app_form.data:
        given_name = app_form.data.get("passport_details.given_name")
        surname = app_form.data.get("passport_details.surname")
        if given_name and surname:
            applicant = f"{surname} {given_name}"

    return ("<b>Заявка на получение визы</b>\n"
            f"От: @{app_form.user.user_name}\n\n"
            f"{visa_summary(app_form.visa)}\n\n"
            f"Заявитель:\n"
            f"<code>{applicant}</code>\n\n"
            f"Создана:\n"
            f"{app_form.created_at.strftime(DATE_TIME_FORMAT)}\n\n"
            f"Последнее изменение:\n"
            f"{app_form.updated_at.strftime(DATE_TIME_FORMAT)}"
            f"Статус: {app_form_status(app_form.status)}")


def app_form_actions_kb(app_form: AppForm, *,
                        current_user: User,
                        to_menu: bool = False) -> InlineKeyboardMarkup:
    keyboard = []
    if app_form.status == AppFormStatus.DRAFT:
        keyboard += [[InlineKeyboardButton(text=buttons.TRASH, callback_data="trash_ask"),
                      InlineKeyboardButton(text=buttons.EDIT, callback_data="edit"),
                      InlineKeyboardButton(text=buttons.SUBMIT, callback_data="submit")]]

    if not is_admin(current_user) and app_form.status == AppFormStatus.PENDING:
        keyboard += [[InlineKeyboardButton(text=buttons.RETURN, callback_data="return")]]

    if is_admin(current_user):
        keyboard += [[InlineKeyboardButton(text=buttons.USER, callback_data=f"user:{app_form.user_id}")]]
        match app_form.status:
            case AppFormStatus.PENDING:
                keyboard += [[InlineKeyboardButton(text=buttons.REJECT, callback_data="reject"),
                              InlineKeyboardButton(text=buttons.ACCEPT, callback_data="accept")]]

            case AppFormStatus.ACCEPTED:
                keyboard += [[InlineKeyboardButton(text=buttons.DONE, callback_data="done")]]

            case AppFormStatus.TRASH:
                keyboard += [[InlineKeyboardButton(text=buttons.RESTORE, callback_data="restore"),
                              InlineKeyboardButton(text=buttons.TRASH, callback_data="delete_ask")]]

    if to_menu:
        keyboard += [[InlineKeyboardButton(text=buttons.TO_MENU, callback_data="to_menu")]]
    else:
        keyboard += [[InlineKeyboardButton(text=buttons.BACK, callback_data="back")]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
