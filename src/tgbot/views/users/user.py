from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.users import User, UserRole
from src.tgbot.views.buttons import BLOCK, SET_ROLE, UNBLOCK, USER_APP_FORMS
from src.tgbot.views.const import DATE_TIME_FORMAT


def is_admin(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]


async def show_user(user: User, *,
                    order_count: int,
                    current_user: User,
                    message: Message,
                    replace: bool = False) -> Message:
    text = user_summary(user)
    reply_markup = user_actions_kb(user,
                                   order_count=order_count,
                                   current_user=current_user)
    if replace:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def user_role(role: UserRole) -> str:
    return {
        UserRole.BLOCKED: "Заблокирован",
        UserRole.USER: "Пользователь",
        UserRole.AGENT: "Агент",
        UserRole.ADMINISTRATOR: "Администратор",
    }.get(role, f"{role}")


def user_summary(user: User) -> str:
    return (f"<b>Пользователь</b> @{user.user_name}\n\n"
            f"<b>Роль:</b> {user_role(user.role)}\n"
            f"<b>Имя:</b> {user.first_name} {user.last_name or ''}\n"
            f"<b>ID:</b> #{user.id}\n"
            f"<b>Telegram ID:</b> {user.telegram_id}\n"
            f"<b>Chat ID:</b> {user.chat_id or '-'}\n\n"
            f"Первый вход: {user.created_at.strftime(DATE_TIME_FORMAT)}\n"
            f"Изменён: {user.updated_at.strftime(DATE_TIME_FORMAT)}\n")


def user_actions_kb(user: User, *, order_count: int, current_user: User) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=f"{USER_APP_FORMS} ({order_count})", callback_data="app_forms")]]
    if current_user.role == UserRole.ADMINISTRATOR:
        if user.id != current_user.id:
            keyboard.append([InlineKeyboardButton(text=BLOCK, callback_data="block")])
        if user.role == UserRole.BLOCKED:
            keyboard.append([InlineKeyboardButton(text=UNBLOCK, callback_data="unblock")])
        keyboard.append([InlineKeyboardButton(text=SET_ROLE, callback_data="set_role")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
