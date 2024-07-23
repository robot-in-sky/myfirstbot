from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.entities.choices import OrderStatus
from app.entities.order import Order
from app.entities.query import CountResultItem, QueryResult
from app.entities.user import User
from app.tgbot.buttons import (
    BACK,
    FILTER,
    FILTER_CHECKED,
    FILTER_CHECKMARK,
    PAGE_NEXT,
    PAGE_PREV,
    SEARCH,
    SEARCH_RESET,
    TO_MENU,
)
from app.tgbot.callbacks import (
    OrderCallbackData,
    OrderFilterCallbackData,
    OrderSearchCallbackData,
    OrdersCallbackData,
)
from app.tgbot.definitions import BUTTON_TEXT_MAX_LEN, COLUMN_DELIMITER
from app.tgbot.utils.helpers import cut_string
from app.tgbot.views.order.order import order_status
from app.tgbot.views.user.user import is_admin


def get_orders_title(user_id: int | None, current_user: User) -> str:
    if user_id:
        if user_id == current_user.id:
            return "Мои заказы"
        return f"Заказы пользователя {user_id}"
    return "Заказы"


async def show_order_filter(  # noqa: PLR0913
        count_by_status: Sequence[CountResultItem[OrderStatus]],
        total_count: int,
        callback_data: OrderFilterCallbackData,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:
    params = callback_data.model_dump(exclude_none=True, exclude={"status"})
    params_back = callback_data.model_dump(exclude_none=True)
    keyboard = []
    for item in count_by_status:
        check_mark = FILTER_CHECKMARK if item.value == callback_data.status else ""
        keyboard += [[InlineKeyboardButton(
                        text=f"{check_mark}  {order_status(item.value)} ({item.count})",
                        callback_data=OrdersCallbackData(status=item.value, **params).pack(),
                    )]]
    keyboard += [[InlineKeyboardButton(
                    text=BACK,
                    callback_data=OrdersCallbackData(**params_back).pack()),
                  InlineKeyboardButton(
                    text=f"Все ({total_count})",
                    callback_data=OrdersCallbackData(**params).pack())]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = get_orders_title(callback_data.user_id, current_user) + "\n"
    if callback_data.s:
        text += f"Поиск: {callback_data.s}\n"
    text += "Фильтр: выберите статус"
    if replace_text:
        await message.edit_text(text, reply_markup=reply_markup)
        return message
    return await message.answer(
        text, reply_markup=reply_markup)


async def show_orders(  # noqa: PLR0913
        result: QueryResult[Order],
        callback_data: OrdersCallbackData,
        notice: str | None = None,
        *,
        current_user: User,
        message: Message,
        replace_text: bool = False,
) -> Message:
    reply_markup = orders_result_kb(result, callback_data, current_user=current_user)
    text = ""
    if notice:
        text += f"ℹ <i>{notice}</i>\n\n"
    text += get_orders_title(callback_data.user_id, current_user) + "\n"
    if len(result.items) > 0:
        if callback_data.s:
            text += f"Поиск: {callback_data.s}\n"
        if callback_data.status:
            text += f"Фильтр: {order_status(callback_data.status)}\n"
        if replace_text:
            await message.edit_text(text, reply_markup=reply_markup)
            return message
        return await message.answer(text, reply_markup=reply_markup)
    text += "Результатов не найдено"
    return await message.answer(text, reply_markup=reply_markup)


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
    keyboard.append(pagination_buttons(result, callback_data))
    keyboard.append(footer_buttons(callback_data))
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
        result: QueryResult[Order],
        callback_data: OrdersCallbackData,
) -> list[InlineKeyboardButton]:
    if (result.page is not None and
            result.total_pages is not None and result.total_pages > 1):
        params = callback_data.model_dump(exclude={"page"})
        prev_page = result.page - 1 if result.page > 1 else result.total_pages
        next_page =result.page + 1 if result.page < result.total_pages else 1
        prev_cb = OrdersCallbackData(page=prev_page, **params).pack()
        next_cb = OrdersCallbackData(page=next_page, **params).pack()
        page_info = f"{result.page}/{result.total_pages}"
        return [InlineKeyboardButton(text=PAGE_PREV, callback_data=prev_cb),
                InlineKeyboardButton(text=page_info, callback_data="_"),
                InlineKeyboardButton(text=PAGE_NEXT, callback_data=next_cb)]
    return []


def footer_buttons(callback_data: OrdersCallbackData) -> list[InlineKeyboardButton]:
    keyboard = [InlineKeyboardButton(text=TO_MENU, callback_data="to_menu")]

    params = callback_data.model_dump(exclude={"page"})
    filter_cb = OrderFilterCallbackData(**params).pack()
    filter_text = FILTER if callback_data.status is None else FILTER_CHECKED
    keyboard += [InlineKeyboardButton(text=filter_text, callback_data=filter_cb)]

    if callback_data.s is None:
        search_cb = OrderSearchCallbackData(**params).pack()
        search_text = SEARCH
    else:
        _params = callback_data.model_dump(exclude={"page", "s"})
        search_cb = OrdersCallbackData(**_params).pack()
        search_text = SEARCH_RESET
    keyboard += [InlineKeyboardButton(text=search_text, callback_data=search_cb)]

    return keyboard
