from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService, UserService
from myfirstbot.tgbot.callbacks import OrdersCallbackData, UserCallbackData
from myfirstbot.tgbot.routers.order.orders import orders_query_handler
from myfirstbot.tgbot.views.user.user import show_user

router = Router()


@router.callback_query(UserCallbackData.filter(~F.action))
async def user_callback(
        query: CallbackQuery,
        callback_data: UserCallbackData,
        db: Database,
        current_user: User,
) -> None:
    user = await UserService(db, current_user).get(callback_data.id)
    order_count = await OrderService(db, current_user).get_count(user.id)
    await query.answer()
    if isinstance(query.message, Message):
        await show_user(user,
                        order_count,
                        current_user=current_user,
                        message=query.message)


@router.callback_query(UserCallbackData.filter(F.action == "get_orders"))
async def user_get_orders_callback(
    query: CallbackQuery,
    callback_data: UserCallbackData,
    db: Database,
    current_user: User,
) -> None:
    await query.answer()
    if isinstance(query.message, Message):
        _callback_data = OrdersCallbackData(user_id=callback_data.id)
        await orders_query_handler(_callback_data,
                                   db=db,
                                   current_user=current_user,
                                   message=query.message)
