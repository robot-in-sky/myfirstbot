from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.choices import UserRole
from src.entities.user import User
from src.tgbot.callbacks import OrdersCallbackData, UserCallbackData
from src.tgbot.views.buttons import BLOCK, SET_ROLE, UNBLOCK, USER_ORDERS
from src.tgbot.views.const import DATE_TIME_FORMAT


def is_admin(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]


async def show_user(  # noqa: PLR0913
        user: User,
        order_count: int,
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
    reply_markup = user_actions_kb(user, order_count, current_user=current_user)
    if replace_text:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


def user_role(role: UserRole) -> str:
    return {
        UserRole.BLOCKED: "Заблокирован",
        UserRole.USER: "Пользователь",
        UserRole.AGENT: "Агент",
        UserRole.ADMINISTRATOR: "Администратор",
    }.get(role, f"<{role}>")


def user_summary(user: User) -> str:
    lines = [
        f"<b>Пользователь</b> @{user.user_name}",
        "",
        f"<b>Роль:</b> {user_role(user.role)}",
        f"<b>Имя:</b> {user.first_name} {user.last_name or ''}",
        f"<b>ID:</b> #{user.id}",
        f"<b>Telegram ID:</b> {user.telegram_id}",
        f"<b>Chat ID:</b> {user.chat_id or '-'}",
        "",
        f"Первый вход: {user.created_at.strftime(DATE_TIME_FORMAT)}",
        f"Изменён: {user.updated_at.strftime(DATE_TIME_FORMAT)}",
    ]
    return "\n".join(lines)


def user_actions_kb(user: User, order_count: int, *, current_user: User) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(
        text=f"{USER_ORDERS} ({order_count})",
        callback_data=OrdersCallbackData(user_id=user.id).pack()),
    ]]
    if current_user.role == UserRole.ADMINISTRATOR:
        if user.id != current_user.id:
            keyboard.append([InlineKeyboardButton(
                text=BLOCK,
                callback_data=UserCallbackData(id=user.id, set_role=UserRole.BLOCKED).pack()),
            ])
        if user.role == UserRole.BLOCKED:
            keyboard.append([InlineKeyboardButton(
                text=UNBLOCK,
                callback_data=UserCallbackData(id=user.id, set_role=UserRole.USER).pack()),
            ])
        keyboard.append([InlineKeyboardButton(
            text=SET_ROLE,
            callback_data=UserCallbackData(id=user.id, set_role=UserRole.USER).pack()),
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
