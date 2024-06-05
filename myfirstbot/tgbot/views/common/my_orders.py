from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order
from myfirstbot.entities.query import QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.views.common import buttons
from myfirstbot.tgbot.views.utils.helpers import cut_string, order_status, is_admin


def order_summary(order: Order, user: User) -> str:
    output = ""
    if is_admin(user):
        output += f"Клиент: {order.user_id}\n"
    output += (
        f"Надпись: {order.label}\n"
        f"Размер: {order.size}\n"
        f"Количество: {order.qty}\n\n"
        f"Статус: {order_status(order.status)}"
    )
    return output


def order_actions_kb(order: Order, user: User) -> InlineKeyboardMarkup:
    keyboard = []
    match order.status:
        case OrderStatus.DRAFT:
            keyboard.append([InlineKeyboardButton(
                text=buttons.SUBMIT, callback_data=f"my_orders:order:submit:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.EDIT, callback_data=f"my_orders:order:edit:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.DELETE, callback_data=f"my_orders:order:trash:{order.id}")])

        case OrderStatus.PENDING:
            keyboard.append([InlineKeyboardButton(
                text=buttons.RETURN, callback_data=f"my_orders:order:return:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.AGENT, callback_data=f"my_orders:order:agent:{order.id}")])

    match order.status:
        case OrderStatus.DRAFT:
            keyboard.append([InlineKeyboardButton(
                text=buttons.SUBMIT, callback_data=f"my_orders:order:submit:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.EDIT, callback_data=f"my_orders:order:edit:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.DELETE, callback_data=f"my_orders:order:trash:{order.id}")])

        case OrderStatus.PENDING:
            keyboard.append([InlineKeyboardButton(
                text=buttons.ACCEPT, callback_data=f"order:accept:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.REJECT, callback_data=f"order:reject:{order.id}")])

        case OrderStatus.ACCEPTED:
            keyboard.append([InlineKeyboardButton(
                text=buttons.DONE, callback_data=f"order:done:{order.id}")])

        case OrderStatus.TRASH:
            keyboard.append([InlineKeyboardButton(
                text=buttons.RESTORE, callback_data=f"order:restore:{order.id}")])
            keyboard.append([InlineKeyboardButton(
                text=buttons.DELETE, callback_data=f"order:delete:{order.id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def order_item_text(order: Order, user: User) -> str:
    columns = {"id": f"#{order.id}"}
    if is_admin(user):
        columns["user_id"] = order.user_id
    columns["summary"] = f" ({order.size})"
    columns["qty"] = f"{order.qty} шт."
    columns["status"] = order_status(order.status)
    delimiter = " | "
    max_width = 45
    label_max_len = max_width - len(delimiter.join(columns.values()))
    label = f"{cut_string(order.label, label_max_len)}"
    columns["summary"] = label + columns["summary"]
    return delimiter.join(columns.values())


def order_items_kb(result: QueryResult[Order], user: User) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=order_item_text(order, user),
            callback_data=f"my_orders:order:get:{order.id}"
        )] for order in result.items]
    page_info = f"{result.page}/{result.total_pages}"
    prev_page = result.page - 1 if result.page > 1 else result.total_pages
    next_page = result.page + 1 if result.page < result.total_pages else 1
    keyboard.append([
        InlineKeyboardButton(text="<", callback_data=f"my_orders:page_prev:{prev_page}"),
        InlineKeyboardButton(text=page_info, callback_data="_"),
        InlineKeyboardButton(text=">", callback_data=f"my_orders:page_next:{next_page}"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
