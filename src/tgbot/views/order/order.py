from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.order import Order, OrderStatus
from src.entities.user import User
from src.tgbot.callbacks import OrderCallbackData, UserCallbackData
from src.tgbot.views import buttons
from src.tgbot.views.const import DATE_TIME_FORMAT
from src.tgbot.views.user.user import is_admin


async def show_order(  # noqa: PLR0913
        order: Order,
        notice: str | None = None,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
        to_menu: bool = False,
) -> Message:
    text = ""
    if notice:
        text += f"ℹ <i>{notice}</i>\n\n"
    text += order_summary(order)
    reply_markup = order_actions_kb(order, current_user=current_user, to_menu=to_menu)
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
        f"Пользователь: @{order.user.user_name}",
        f"Создан: {order.created_at.strftime(DATE_TIME_FORMAT)}",
        f"Изменен: {order.updated_at.strftime(DATE_TIME_FORMAT)}",
    ]
    return "\n".join(lines)


def order_actions_kb(
        order: Order,
        *,
        current_user: User,
        to_menu: bool = False,
) -> InlineKeyboardMarkup:

    def action_button(text: str, action: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=text, callback_data=OrderCallbackData(id=order.id, action=action).pack())

    user_button = InlineKeyboardButton(
            text=buttons.USER, callback_data=UserCallbackData(id=order.user_id).pack())

    keyboard = [[InlineKeyboardButton(text=buttons.PAGE_PREV, callback_data="_"),
                 InlineKeyboardButton(
                    text=buttons.DUPLICATE,
                    callback_data=OrderCallbackData(id=order.id, action="duplicate_ask").pack()),
                 InlineKeyboardButton(text=buttons.PAGE_NEXT, callback_data="_")]]

    if order.status == OrderStatus.DRAFT:
        keyboard += [[action_button(buttons.TRASH, "trash_ask"),
                      action_button(buttons.EDIT, "edit"),
                      action_button(buttons.SUBMIT, "submit")]]

    if not is_admin(current_user) and order.status == OrderStatus.PENDING:
        keyboard += [[action_button(buttons.RETURN, "return")]]

    if is_admin(current_user):
        match order.status:
            case OrderStatus.PENDING:
                keyboard += [[user_button,
                              action_button(buttons.REJECT, "reject"),
                              action_button(buttons.ACCEPT, "accept")]]

            case OrderStatus.ACCEPTED:
                keyboard += [[user_button,
                              action_button(buttons.DONE, "done")]]

            case OrderStatus.TRASH:
                keyboard += [[user_button,
                              action_button(buttons.RESTORE, "restore"),
                              action_button(buttons.TRASH, "delete_ask")]]

    if to_menu:
        keyboard += [[InlineKeyboardButton(text=buttons.TO_MENU, callback_data="to_menu")]]
    else:
        keyboard += [[action_button(buttons.BACK, "back")]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
