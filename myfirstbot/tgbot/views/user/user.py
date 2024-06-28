from aiogram.types import InlineKeyboardMarkup, Message

from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.user import User


def is_admin(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]


async def show_user(
        user: User,
        notice: str | None = None,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:
    text = ""
    if notice:
        text += f"<i>{notice}</i>\n\n"
    text += user_summary(user)
    keyboard = user_actions_kb(user, current_user)
    if replace_text:
        await message.edit_text(text, reply_markup=keyboard)
        return message
    return await message.answer(text, reply_markup=keyboard)


def user_role(role: UserRole) -> str:
    return {
        UserRole.BLOCKED: "Заблокирован",
        UserRole.USER: "Пользователь",
        UserRole.AGENT: "Агент",
        UserRole.ADMINISTRATOR: "Администратор",
    }.get(role, f"<{role}>")


def user_summary(user: User) -> str:
    lines = [
        f"<b>Пользователь #{user.id}</b>",
        "",
        f"<b>Юзернейм:</b> {user.user_name}",
        f"<b>Имя:</b> {user.first_name}",
        f"<b>Фамилия:</b> {user.last_name}",
        f"<b>Роль:</b> {user_role(user.role)}",
        "",
        f"<b>Первый вход:</b> {user.created.strftime("%m.%d.%Y %H:%M")}",
        f"<b>Данные изменены:</b> {user.updated.strftime("%m.%d.%Y %H:%M")}",
    ]
    return "\n".join(lines)


def user_actions_kb(user: User, current_user: User) -> InlineKeyboardMarkup:
    keyboard = []
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
