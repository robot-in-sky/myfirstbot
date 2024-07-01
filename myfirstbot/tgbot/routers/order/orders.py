from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.buttons import ALL_ORDERS, MY_ORDERS
from myfirstbot.tgbot.callbacks import OrdersCallbackData
from myfirstbot.tgbot.views.order.orders import orders_result_kb, show_order_filter, show_orders

router = Router()


async def orders_query_handler(
        callback_data: OrdersCallbackData,
        *,
        db: Database,
        current_user: User,
        message: Message,
) -> None:
    service = OrderService(db, current_user)
    get_count_params = callback_data.model_dump(exclude_none=True, exclude={"page", "per_page"})
    count_by_status = await service.get_count_by_status(**get_count_params)
    if len(count_by_status) > 1:
        total_count = await service.get_count(**get_count_params)
        await show_order_filter(count_by_status,
                                total_count,
                                callback_data,
                                current_user=current_user,
                                message=message)
    else:
        get_all_params = callback_data.model_dump(exclude_none=True)
        result = await service.get_all(**get_all_params)
        await show_orders(result, callback_data,
                          current_user=current_user,
                          message=message)


@router.message(F.text == MY_ORDERS)
async def my_orders_button_handler(
        message: Message,
        db: Database,
        current_user: User,
) -> None:
    callback_data = OrdersCallbackData(user_id=current_user.id)
    await orders_query_handler(callback_data, db=db,
                               current_user=current_user,
                               message=message)


@router.message(F.text == ALL_ORDERS)
async def all_orders_button_handler(
        message: Message,
        db: Database,
        current_user: User,
) -> None:
    callback_data = OrdersCallbackData()
    await orders_query_handler(callback_data, db=db,
                               current_user=current_user,
                               message=message)


@router.callback_query(OrdersCallbackData.filter())
async def orders_callback(
        query: CallbackQuery,
        callback_data: OrdersCallbackData,
        db: Database,
        current_user: User,
) -> None:
    params = callback_data.model_dump(exclude_none=True)
    result = await OrderService(db, current_user).get_all(**params)
    await query.answer()
    if isinstance(query.message, Message):
        if callback_data.page:
            await query.message.edit_reply_markup(
                reply_markup=orders_result_kb(result, callback_data,
                                              current_user=current_user))
        else:
            await show_orders(result,
                              callback_data,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)
