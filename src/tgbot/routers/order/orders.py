from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.choices import UserRole
from src.entities.order import OrderQuery, OrderQueryPaged
from src.entities.user import User
from src.services import OrderService
from src.tgbot.views.buttons import MY_ORDERS, ORDERS
from src.tgbot.callbacks import OrderFilterCallbackData, OrderSearchCallbackData, OrdersCallbackData
from src.tgbot.scenes import SearchOrderScene
from src.tgbot.views.order.orders import orders_result_kb, show_order_filter, show_orders

router = Router()
scene_registry = SceneRegistry(router)


@router.message(F.text.in_({MY_ORDERS, ORDERS}))
async def orders_button_handler(
        message: Message,
        deps: Dependencies,
        current_user: User,
) -> None:
    callback_data = OrdersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    if message.text == MY_ORDERS or current_user.role < UserRole.AGENT:
        params["user_id"] = current_user.id
    result = await OrderService(deps, current_user).get_many(OrderQueryPaged(**params))
    await show_orders(result,
                      callback_data,
                      current_user=current_user,
                      message=message)


@router.callback_query(OrdersCallbackData.filter())
async def orders_callback_handler(
        query: CallbackQuery,
        callback_data: OrdersCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    await query.answer()
    params = callback_data.model_dump(exclude_none=True)
    if current_user.role < UserRole.AGENT:
        params["user_id"] = current_user.id
    result = await OrderService(deps, current_user).get_many(OrderQueryPaged(**params))
    if isinstance(query.message, Message):
        if callback_data.page:
            await query.message.edit_reply_markup(
                reply_markup=orders_result_kb(result,
                                              callback_data,
                                              current_user=current_user))
        else:
            await show_orders(result,
                              callback_data,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)


scene_registry.add(SearchOrderScene)
router.callback_query.register(
    SearchOrderScene.as_handler(), OrderSearchCallbackData.filter())


@router.callback_query(OrderFilterCallbackData.filter())
async def order_filter_callback_handler(
        query: CallbackQuery,
        callback_data: OrderFilterCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    await query.answer()
    if isinstance(query.message, Message):
        service = OrderService(deps, current_user)
        params = callback_data.model_dump(
            exclude_none=True,
            exclude={"status", "page", "per_page"},
        )
        if current_user.role < UserRole.AGENT:
            params["user_id"] = current_user.id
        count_by_status = await service.get_count_by_status(OrderQuery(**params))
        total_count = await service.get_count(OrderQuery(**params))
        await show_order_filter(count_by_status,
                                total_count,
                                callback_data,
                                current_user=current_user,
                                message=query.message,
                                replace_text=True)
