from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.order import Order
from myfirstbot.entities.query import QueryResult
from myfirstbot.entities.user import User
from myfirstbot.tgbot.buttons import PAGE_NEXT, PAGE_PREV
from myfirstbot.tgbot.callbacks import AllOrdersCallbackData, MyOrdersCallbackData, OrderCallbackData
from myfirstbot.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from myfirstbot.tgbot.utils.helpers import cut_string
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.order.order import order_status
from myfirstbot.tgbot.views.user.user import is_admin


async def show_my_orders(
        result: QueryResult,
        callback_data: MyOrdersCallbackData,
        *,
        current_user: User,
        message: Message,
) -> Message:
    if len(result.items) > 0:
        keyboard = orders_result_kb(result, callback_data, current_user=current_user)
        if callback_data.page:
            await message.edit_reply_markup(reply_markup=keyboard)
            return message
        lines = ["Мои заказы"]
        if callback_data.status:
            lines.append(f"Статус: {order_status(callback_data.status)}")
        text = "\n".join(lines)
        return await message.answer(text, reply_markup=keyboard)
    return await message.answer("У Вас ещё нет заказов",
                                reply_markup=main_menu_kb(current_user))


async def show_all_orders(
        result: QueryResult[Order],
        callback_data: AllOrdersCallbackData,
        *,
        current_user: User,
        message: Message,
) -> Message:

    if len(result.items) > 0:
        keyboard = orders_result_kb(result, callback_data, current_user=current_user)
        if callback_data.page:
            await message.edit_reply_markup(reply_markup=keyboard)
            return message
        lines = ["Все заказы"]
        if callback_data.user_id:
            lines.append(f"Пользователь: {callback_data.user_id}")
        if callback_data.status:
            lines.append(f"Статус: {order_status(callback_data.status)}")
        text = "\n".join(lines)
        return await message.answer(text, reply_markup=keyboard)
    return await message.answer("Заказы не найдены",
                                reply_markup=main_menu_kb(current_user))


def orders_result_kb(
        result: QueryResult[Order],
        callback_data: MyOrdersCallbackData | AllOrdersCallbackData,
        *,
        current_user: User,
) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text=order_item_text(order, current_user),
            callback_data=OrderCallbackData(id=order.id).pack(),
        )] for order in result.items]
    if result.total_pages > 1:
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


def pagination_buttons(
        result: QueryResult,
        callback_data: MyOrdersCallbackData | AllOrdersCallbackData,
) -> list[InlineKeyboardButton]:
    callback_page = callback_data.page
    callback_data.page = result.page - 1 if result.page > 1 else result.total_pages
    callback_prev = callback_data.pack()
    callback_data.page = result.page + 1 if result.page < result.total_pages else 1
    callback_next = callback_data.pack()
    callback_data.page = callback_page
    page_info = f"{result.page}/{result.total_pages}"
    return [InlineKeyboardButton(text=PAGE_PREV, callback_data=callback_prev),
            InlineKeyboardButton(text=page_info, callback_data="_"),
            InlineKeyboardButton(text=PAGE_NEXT, callback_data=callback_next)]
