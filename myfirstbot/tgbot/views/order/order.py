from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order
from myfirstbot.entities.user import User
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.callbacks import OrderCallbackData
from myfirstbot.tgbot.views.user.user import is_admin


async def show_order(
        order: Order,
        notice: str | None = None,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:
    text = ""
    if notice:
        text += f"<i>{notice}</i>\n\n"
    text += order_summary(order)
    keyboard = order_actions_kb(order, current_user)
    if replace_text:
        await message.edit_text(text, reply_markup=keyboard)
        return message
    return await message.answer(text, reply_markup=keyboard)


def order_status(status: OrderStatus) -> str:
    return {
        OrderStatus.TRASH: "Удалён",
        OrderStatus.DRAFT: "Черновик",
        OrderStatus.PENDING: "На проверке",
        OrderStatus.ACCEPTED: "В работе",
        OrderStatus.COMPLETED: "Завершён",
    }.get(status, f"<{status}>")


def order_summary(order: Order) -> str:
    lines = [
        f"<b>Заказ #{order.id}</b>",
        "",
        f"<b>Надпись:</b> {order.label}",
        f"<b>Размер:</b> {order.size}",
        f"<b>Количество:</b> {order.qty}",
        "",
        f"<b>Статус:</b> {order_status(order.status)}",
        f"<b>Создан:</b> {order.created.strftime("%m.%d.%Y %H:%M")}",
        f"<b>Изменен:</b> {order.updated.strftime("%m.%d.%Y %H:%M")}",
    ]
    return "\n".join(lines)


def order_actions_kb(order: Order, current_user: User) -> InlineKeyboardMarkup:
    rows = []

    if order.status == OrderStatus.DRAFT:
        rows.append([(buttons.EDIT, "edit"), (buttons.DELETE, "trash_ask")])
        rows.append([(buttons.SUBMIT, "submit")])

    if not is_admin(current_user) and order.status == OrderStatus.PENDING:
        rows.append([(buttons.RETURN, "return"), (buttons.AGENT, "agent")])

    if is_admin(current_user):
        match order.status:
            case OrderStatus.PENDING:
                rows.append([(buttons.ACCEPT, "accept")])
                rows.append([(buttons.REJECT, "reject")])
            case OrderStatus.ACCEPTED:
                rows.append([(buttons.DONE, "done")])
            case OrderStatus.TRASH:
                rows.append([(buttons.RESTORE, "restore"), (buttons.DELETE, "delete")])

    rows.append([(buttons.TO_MENU, "to_menu")])

    keyboard = []
    for row in rows:
        keyboard_row = [InlineKeyboardButton(
            text=t[0],
            callback_data=OrderCallbackData(id=order.id, action=t[1]).pack(),
        ) for t in row]
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
