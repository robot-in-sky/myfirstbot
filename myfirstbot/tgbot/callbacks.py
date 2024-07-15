from aiogram.filters.callback_data import CallbackData

from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.tgbot.definitions import PER_PAGE_DEFAULT


class UsersCallbackData(CallbackData, prefix="users"):
    role: UserRole | None = None
    s: str | None = None
    page: int | None = None
    per_page: int = PER_PAGE_DEFAULT


class UserFilterCallbackData(UsersCallbackData, prefix="user_filter"):
    pass


class UserSearchCallbackData(UsersCallbackData, prefix="user_search"):
    pass


class UserCallbackData(CallbackData, prefix="user"):
    id: int
    set_role: UserRole | None = None


class OrdersCallbackData(CallbackData, prefix="orders"):
    user_id: int | None = None
    status: OrderStatus | None = None
    s: str | None = None
    page: int | None = None
    per_page: int = PER_PAGE_DEFAULT


class OrderFilterCallbackData(OrdersCallbackData, prefix="order_filter"):
    pass


class OrderSearchCallbackData(OrdersCallbackData, prefix="order_search"):
    pass


class OrderCallbackData(CallbackData, prefix="order"):
    id: int
    action: str | None = None


class EditorCallbackData(CallbackData, prefix="editor"):
    action: str
