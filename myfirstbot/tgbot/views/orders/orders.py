from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from myfirstbot.entities.order import Order
from myfirstbot.entities.query import QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.buttons import BTN_TEXT_MAX_LEN, COLUMN_DELIMITER, PAGE_NEXT, PAGE_INFO_TEMPLATE, PAGE_PREV
from myfirstbot.tgbot.views.orders.order import order_status
from myfirstbot.tgbot.views.users.user import is_admin
from myfirstbot.tgbot.utils.helpers import cut_string


def order_item_text(order: Order, user: User) -> str:
    columns = {"id": f"#{order.id}"}
    if is_admin(user):
        columns["user_id"] = str(order.user_id)
    columns["summary"] = f" ({order.size})"
    columns["qty"] = f"{order.qty} шт."
    columns["status"] = order_status(order.status)
    label_max_len = BTN_TEXT_MAX_LEN - len(COLUMN_DELIMITER.join(columns.values()))
    label = f"{cut_string(order.label, label_max_len)}"
    columns["summary"] = label + columns["summary"]
    return COLUMN_DELIMITER.join(columns.values())


def order_items_kb(result: QueryResult[Order], user: User, target: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=order_item_text(order, user),
            callback_data=f"order:get:{order.id}"
        )] for order in result.items]
    page_info = PAGE_INFO_TEMPLATE % (result.page, result.total_pages)
    prev_page = result.page - 1 if result.page > 1 else result.total_pages
    next_page = result.page + 1 if result.page < result.total_pages else 1
    keyboard.append([
        InlineKeyboardButton(text=PAGE_PREV, callback_data=f"{target}:page_prev:{prev_page}"),
        InlineKeyboardButton(text=page_info, callback_data="_"),
        InlineKeyboardButton(text=PAGE_NEXT, callback_data=f"{target}:page_next:{next_page}"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
