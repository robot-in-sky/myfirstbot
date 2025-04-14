from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.users import User
from src.entities.visas import AppForm, AppFormStatus, Visa
from src.tgbot.views import buttons
from src.tgbot.views.const import DATE_TIME_FORMAT
from src.tgbot.views.users.user import is_admin
from src.tgbot.views.visas.apply_visa import visa_summary


async def show_app_form(app_form: AppForm, *,
                        current_user: User,
                        message: Message,
                        replace: bool = False,
                        back: bool = True) -> Message:
    text = app_form_summary(app_form)
    reply_markup = app_form_actions_kb(app_form, current_user=current_user, back=back)
    # await message.answer(str(app_form.data))
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def app_form_status(status: AppFormStatus) -> str:
    return {
        AppFormStatus.TRASH: "Удалёно",
        AppFormStatus.DRAFT: "Заполняется",
        AppFormStatus.SAVED: "Ожидает оплаты",
        AppFormStatus.PENDING: "На проверке",
        AppFormStatus.ACCEPTED: "В работе",
        AppFormStatus.COMPLETED: "Завершёно",
    }.get(status, f"{status}")


def app_form_applicant_data(app_form: AppForm) -> dict[str, str] | None:
    if app_form.data:
        given_name = app_form.data.get("form.data.applicant_details.given_name")
        surname = app_form.data.get("form.data.applicant_details.surname")
        birth_date = app_form.data.get("form.data.applicant_details.birth_date", "")
        birth_year = birth_date.split("-")[0] if "-" in birth_date else None
        if given_name and surname:
            return {"given_name": given_name,
                    "surname": surname,
                    "birth_year": birth_year}
    return None


def app_form_summary(app_form: AppForm) -> str:
    applicant = ""
    if data := app_form_applicant_data(app_form):
        applicant = ("<b>Заявитель</b>:\n"
                     f"{data["given_name"]} {data["surname"]} ({data["birth_year"]})\n\n")

    summary = ""
    if isinstance(app_form.visa, Visa):
        summary = f"{visa_summary(app_form.visa)}\n"

    return ("<b>Заявка на получение визы</b>\n"
            f"От: @{app_form.user.user_name}\n\n"
            f"{applicant}"
            f"{summary}"
            f"<b>Создана</b>: {app_form.created_at.strftime(DATE_TIME_FORMAT)}\n"
            f"<b>Последнее изменение</b>: {app_form.updated_at.strftime(DATE_TIME_FORMAT)}\n"
            f"<b>Статус</b>: {app_form_status(app_form.status)}")


def app_form_actions_kb(app_form: AppForm, *,
                        current_user: User,
                        back: bool = True) -> InlineKeyboardMarkup:
    keyboard = []
    match app_form.status:
        case AppFormStatus.DRAFT:
            keyboard += [[InlineKeyboardButton(text=buttons.TRASH,
                                               callback_data="action:trash_ask"),
                          InlineKeyboardButton(text=buttons.FORM_CONTINUE,
                                               callback_data="action:continue")]]
        case AppFormStatus.SAVED:
            keyboard += [[InlineKeyboardButton(text=buttons.TRASH,
                                               callback_data="action:trash_ask"),
                          InlineKeyboardButton(text=buttons.DOWNLOAD_PDF,
                                               callback_data="action:download_pdf")]]

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

    if back:
        keyboard += [[InlineKeyboardButton(text=buttons.BACK, callback_data="back")]]
    else:
        keyboard += [[InlineKeyboardButton(text=buttons.TO_MENU, callback_data="to_menu")]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
