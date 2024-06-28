from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.buttons import ALL_ORDERS, MY_ORDERS
from myfirstbot.tgbot.callbacks import AllOrdersCallbackData, MyOrdersCallbackData
from myfirstbot.tgbot.views.order.orders import show_all_orders, show_my_orders

router = Router()


@router.message(F.text == MY_ORDERS)
async def my_orders_button_handler(
        message: Message, db: Database, current_user: User) -> None:
    callback_data = MyOrdersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    result = await OrderService(db, current_user).get_my(**params)
    await show_my_orders(result, callback_data,
                         current_user=current_user,
                         message=message)


@router.callback_query(MyOrdersCallbackData.filter())
async def my_orders_query_callback(
        query: CallbackQuery,
        callback_data: MyOrdersCallbackData,
        db: Database,
        current_user: User,
) -> None:
    await query.answer()
    params = callback_data.model_dump(exclude_none=True)
    result = await OrderService(db, current_user).get_my(**params)
    await show_my_orders(result, callback_data,
                         current_user=current_user,
                         message=query.message)


@router.message(F.text == ALL_ORDERS)
async def all_orders_button_handler(
        message: Message, db: Database, current_user: User) -> None:
    callback_data = AllOrdersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    result = await OrderService(db, current_user).get_all(**params)
    await show_all_orders(result, callback_data,
                          current_user=current_user,
                          message=message)


@router.callback_query(AllOrdersCallbackData.filter())
async def all_orders_query_callback(
        query: CallbackQuery,
        callback_data: AllOrdersCallbackData,
        db: Database,
        current_user: User,
) -> None:
    await query.answer()
    params = callback_data.model_dump(exclude_none=True)
    result = await OrderService(db, current_user).get_all(**params)
    await show_all_orders(result, callback_data,
                          current_user=current_user,
                          message=query.message)
