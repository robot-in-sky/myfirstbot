from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order
from myfirstbot.entities.user import User
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.callbacks import OrderCallbackData
from myfirstbot.tgbot.definitions import DATE_TIME_FORMAT
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
        text += f"ℹ <i>{notice}</i>\n\n"
    text += order_summary(order)
    reply_markup = order_actions_kb(order, current_user)
    if replace_text:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(text, reply_markup=reply_markup)


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
        f"<b>Заказ #{order.id}</b> — {order_status(order.status)}",
        "",
        "<b>Страница 1/1</b>",
        "",
        f"    <b>Надпись:</b> {order.label}    ",
        f"    <b>Размер:</b> {order.size}    ",
        f"    <b>Количество:</b> {order.qty}    ",
        "",
        f"Создан: {order.created.strftime(DATE_TIME_FORMAT)}",
        f"Изменен: {order.updated.strftime(DATE_TIME_FORMAT)}",
    ]
    return "\n".join(lines)


def order_actions_kb(order: Order, current_user: User) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(
                    text=buttons.DUPLICATE,
                    callback_data=OrderCallbackData(id=order.id, action="duplicate_ask").pack()),
                 InlineKeyboardButton(text=buttons.PAGE_PREV, callback_data="_"),
                 InlineKeyboardButton(text=buttons.PAGE_NEXT, callback_data="_")]]

    rows = []
    if order.status == OrderStatus.DRAFT:
        rows.append([(buttons.TRASH, "trash_ask"),
                     (buttons.EDIT, "edit"),
                     (buttons.SUBMIT, "submit")])

    if not is_admin(current_user) and order.status == OrderStatus.PENDING:
        rows.append([(buttons.RETURN, "return")])

    if is_admin(current_user):
        match order.status:
            case OrderStatus.PENDING:
                rows.append([(buttons.ACCEPT, "accept"), (buttons.REJECT, "reject")])
            case OrderStatus.ACCEPTED:
                rows.append([(buttons.DONE, "done")])
            case OrderStatus.TRASH:
                rows.append([(buttons.RESTORE, "restore"), (buttons.TRASH, "delete_ask")])

    rows.append([(buttons.BACK, "back")])

    for row in rows:
        keyboard_row = [InlineKeyboardButton(
            text=t[0],
            callback_data=OrderCallbackData(id=order.id, action=t[1]).pack(),
        ) for t in row]
        keyboard.append(keyboard_row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
