from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.entities.base import QueryResult
from src.tgbot.views.buttons import (
    BACK,
    CANCEL,
    FILTER,
    FILTER_CHECKED,
    NO,
    OK,
    PAGE_NEXT,
    PAGE_PREV,
    SEARCH,
    SEARCH_RESET,
    TO_MENU,
    YES,
)


def pagination_buttons(result: QueryResult[Any]) -> list[InlineKeyboardButton]:
    if (result.page is not None and
            result.total_pages is not None and result.total_pages > 1):
        page_info = f"{result.page}/{result.total_pages}"
        prev_page = result.page - 1 if result.page > 1 else result.total_pages
        next_page = result.page + 1 if result.page < result.total_pages else 1
        return [InlineKeyboardButton(text=PAGE_PREV, callback_data=f"page:{prev_page}"),
                InlineKeyboardButton(text=page_info, callback_data="_"),
                InlineKeyboardButton(text=PAGE_NEXT, callback_data=f"page:{next_page}")]
    return []


def bottom_buttons(*, filter_: bool = False, search: bool = False) -> list[InlineKeyboardButton]:
    keyboard = [InlineKeyboardButton(text=TO_MENU, callback_data="to_menu")]
    filter_text = FILTER_CHECKED if filter_ else FILTER
    keyboard += [InlineKeyboardButton(text=filter_text, callback_data="action:filter")]
    search_text = SEARCH_RESET if search else SEARCH
    keyboard += [InlineKeyboardButton(text=search_text, callback_data="action:search")]
    return keyboard


def back_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=BACK, callback_data="back")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def ok_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=BACK, callback_data="ok")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cancel_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=BACK, callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def ok_cancel_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=CANCEL, callback_data="ok"),
                 InlineKeyboardButton(text=OK, callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def yes_no_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=YES, callback_data="yes"),
                 InlineKeyboardButton(text=NO, callback_data="no")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
