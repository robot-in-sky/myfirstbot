from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.choices import OrderStatus
from myfirstbot.entities.order import Order
from myfirstbot.entities.query import CountedResultItem, QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.buttons import ALL_ORDERS, TRASH
from myfirstbot.tgbot.callbacks import OrderCallbackData, OrdersCallbackData
from myfirstbot.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from myfirstbot.tgbot.utils.helpers import cut_string
from myfirstbot.tgbot.views.common.pagination import pagination_buttons
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.order.order import order_status
from myfirstbot.tgbot.views.user.user import is_admin


def get_orders_title(callback_data: OrdersCallbackData, current_user: User) -> str:
    if callback_data.user_id:
        if callback_data.user_id == current_user.id:
            return "Мои заказы"
        return f"Заказы пользователя {callback_data.user_id}"
    return "Все заказы"


async def show_order_filter(
        count_by_status: Sequence[CountedResultItem[OrderStatus]],
        total_count: int,
        callback_data: OrdersCallbackData,
        *,
        current_user: User,
        message: Message,
) -> Message:
    params = callback_data.model_dump(exclude={"status"})
    keyboard = []

    """Statuses"""
    col = 2
    for i in range(0, len(count_by_status), col):
        row = [InlineKeyboardButton(
                    text=f"{order_status(item.value)} ({item.count})",
                    callback_data = OrdersCallbackData(status=item.value, **params).pack(),
               ) for item in count_by_status[i:i+col] if item.value != OrderStatus.TRASH]
        keyboard.append(row)

    """All orders"""
    keyboard.append([InlineKeyboardButton(
        text=f"{ALL_ORDERS} ({total_count})",
        callback_data=OrdersCallbackData(**params).pack(),
    )])

    """Trash"""
    if trash_item := next(item for item in count_by_status if item.value == OrderStatus.TRASH):
        keyboard.append([InlineKeyboardButton(
            text=f"{TRASH} ({trash_item.count})",
            callback_data=OrdersCallbackData(status=trash_item.value, **params).pack(),
        )])

    text = get_orders_title(callback_data, current_user)
    return await message.answer(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


async def show_orders(
        result: QueryResult[Order],
        callback_data: OrdersCallbackData,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:

    if len(result.items) > 0:
        text = get_orders_title(callback_data, current_user) + "\n"
        if callback_data.status:
            text += f"Статус: {order_status(callback_data.status)}"
        keyboard = orders_result_kb(result, callback_data, current_user=current_user)
        if replace_text:
            await message.edit_text(text, reply_markup=keyboard)
            return message
        return await message.answer(text, reply_markup=keyboard)
    return await message.answer("Заказы не найдены",
                                reply_markup=main_menu_kb(current_user))


def orders_result_kb(
        result: QueryResult[Order],
        callback_data: OrdersCallbackData,
        *,
        current_user: User,
) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=order_item_text(order, current_user),
            callback_data=OrderCallbackData(id=order.id).pack(),
        )] for order in result.items]
    if result.total_pages and result.total_pages > 1:
        keyboard.append(pagination_buttons(result, callback_data))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def order_item_text(order: Order, current_user: User) -> str:
    columns = {"id": f"#{order.id}"}
    if is_admin(current_user):
        columns["user_id"] = str(order.user_id)
    columns["summary"] = f" ({order.size})"
    columns["qty"] = f"{order.qty} шт."
    columns["status"] = order_status(order.status)
    label_max_len = BUTTON_TEXT_MAX_LEN - len(COLUMN_DELIMITER.join(columns.values()))
    label = f"{cut_string(order.label, label_max_len)}"
    columns["summary"] = label + columns["summary"]
    return COLUMN_DELIMITER.join(columns.values())
