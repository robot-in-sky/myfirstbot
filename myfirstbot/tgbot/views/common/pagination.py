from aiogram.types import InlineKeyboardButton

from myfirstbot.entities.query import QueryResult
from myfirstbot.tgbot.buttons import PAGE_NEXT, PAGE_PREV
from myfirstbot.tgbot.callbacks import OrdersCallbackData, UsersCallbackData


def pagination_buttons(
        result: QueryResult,
        callback_data: OrdersCallbackData | UsersCallbackData,
) -> list[InlineKeyboardButton]:
    if result.page is None or result.total_pages is None:
        return []
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
