from aiogram.filters.callback_data import CallbackData

from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.tgbot.definitions import PER_PAGE_DEFAULT


class UsersCallbackData(CallbackData, prefix="users"):
    role: UserRole | None = None
    page: int | None = None
    per_page: int = PER_PAGE_DEFAULT


class UserCallbackData(CallbackData, prefix="user"):
    id: int
    action: str | None = None


class MyOrdersCallbackData(CallbackData, prefix="my_orders"):
    status: OrderStatus | None = None
    page: int | None = None
    per_page: int = PER_PAGE_DEFAULT


class AllOrdersCallbackData(CallbackData, prefix="all_orders"):
    user_id: str | None = None
    status: OrderStatus | None = None
    page: int | None = None
    per_page: int = PER_PAGE_DEFAULT


class OrderCallbackData(CallbackData, prefix="order"):
    id: int
    action: str | None = None


class EditorCallbackData(CallbackData, prefix="editor"):
    action: str
