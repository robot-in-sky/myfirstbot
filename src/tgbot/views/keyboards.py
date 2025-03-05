from typing import Any

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.base import QueryResult
from src.tgbot.views.buttons import (
    CANCEL,
    FILTER,
    FILTER_CHECKED,
    OK,
    PAGE_NEXT,
    PAGE_PREV,
    SEARCH,
    SEARCH_RESET,
    TO_MENU,
)


def pagination_buttons(result: QueryResult[Any]) -> list[InlineKeyboardButton]:
    if (result.page is not None and
            result.total_pages is not None and result.total_pages > 1):
        page_info = f"{result.page}/{result.total_pages}"
        return [InlineKeyboardButton(text=PAGE_PREV, callback_data="prev"),
                InlineKeyboardButton(text=page_info, callback_data="_"),
                InlineKeyboardButton(text=PAGE_NEXT, callback_data="next")]
    return []


def filter_buttons(*, filter_: bool = False, search: bool = False) -> list[InlineKeyboardButton]:
    keyboard = [InlineKeyboardButton(text=TO_MENU, callback_data="to_menu")]
    filter_text = FILTER if filter_ is None else FILTER_CHECKED
    keyboard += [InlineKeyboardButton(text=filter_text, callback_data="filter")]
    search_text = SEARCH if search is None else SEARCH_RESET
    keyboard += [InlineKeyboardButton(text=search_text, callback_data="search")]
    return keyboard


def ok_cancel_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=CANCEL, callback_data="ok"),
                 InlineKeyboardButton(text=OK, callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
