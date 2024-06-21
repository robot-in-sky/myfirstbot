from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.views.users.user import is_admin


def order_status(status: OrderStatus) -> str:
    return {
        OrderStatus.TRASH: "Удалён",
        OrderStatus.DRAFT: "Черновик",
        OrderStatus.PENDING: "На проверке",
        OrderStatus.ACCEPTED: "В работе",
        OrderStatus.COMPLETED: "Завершён",
    }.get(status, f"<{status}>")


def order_summary(order: Order | OrderAdd | OrderUpdate, user: User) -> str:
    output = f"<b>Заказ #{order.id}</b>\n\n"
    # if is_admin(user):
    #     output += f"<b>Клиент:</b> {order.user_id}\n\n"
    output += (
        f"  <b>Надпись:</b> {order.label}\n"
        f"  <b>Размер:</b> {order.size}\n"
        f"  <b>Количество:</b> {order.qty}\n\n"
        f"  <b>Статус:</b> {order_status(order.status)}\n"
        f"  <b>Создан:</b> {order.created.strftime("%m.%d.%Y %H:%M")}\n"
        f"  <b>Изменен:</b> {order.updated.strftime("%m.%d.%Y %H:%M")}\n\n"
    )
    return output


def order_actions_kb(order: Order, user: User) -> InlineKeyboardMarkup:
    keyboard = []

    if order.status == OrderStatus.DRAFT:
        keyboard.append([
            InlineKeyboardButton(
                text=buttons.EDIT, callback_data=f"edit_order:start:{order.id}"),
            InlineKeyboardButton(
                text=buttons.DELETE, callback_data=f"order:trash:{order.id}")
        ])
        keyboard.append([InlineKeyboardButton(
            text=buttons.SUBMIT, callback_data=f"order:submit:{order.id}")])

    if not is_admin(user) and order.status == OrderStatus.PENDING:
            keyboard.append([
                InlineKeyboardButton(
                    text=buttons.RETURN, callback_data=f"order:return:{order.id}"),
                InlineKeyboardButton(
                    text=buttons.AGENT, callback_data=f"order:agent:{order.id}"
            )])

    if is_admin(user):
        match order.status:
            case OrderStatus.PENDING:
                keyboard.append([
                    InlineKeyboardButton(
                        text=buttons.ACCEPT, callback_data=f"order:accept:{order.id}"),
                    InlineKeyboardButton(
                        text=buttons.REJECT, callback_data=f"order:reject:{order.id}")
                ])

            case OrderStatus.ACCEPTED:
                keyboard.append([InlineKeyboardButton(
                    text=buttons.DONE, callback_data=f"order:done:{order.id}")])

            case OrderStatus.TRASH:
                keyboard.append([
                    InlineKeyboardButton(
                        text=buttons.RESTORE, callback_data=f"order:restore:{order.id}"),
                    InlineKeyboardButton(
                        text=buttons.DELETE, callback_data=f"order:delete:{order.id}")
                ])

    keyboard.append([InlineKeyboardButton(
        text=buttons.TO_MENU, callback_data="order:menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
