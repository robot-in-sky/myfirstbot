from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from src.entities.choices import UserRole
from src.entities.order import OrderAdd, OrderQueryPaged
from src.entities.user import User
from src.repositories.utils import Database
from src.services import OrderService
from src.tgbot import buttons
from src.tgbot.callbacks import OrderCallbackData, OrdersCallbackData
from src.tgbot.scenes import EditOrderScene, NewOrderScene
from src.tgbot.views.common.ok_cancel import ok_cancel_kb
from src.tgbot.views.order.order import show_order
from src.tgbot.views.order.orders import show_orders

router = Router()
scene_registry = SceneRegistry(router)


scene_registry.add(NewOrderScene)
router.message.register(
    NewOrderScene.as_handler(), F.text == buttons.NEW_ORDER)
router.callback_query.register(
    NewOrderScene.as_handler(), F.data == "new_order")


@router.callback_query(OrderCallbackData.filter(~F.action))
async def order_callback_handler(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        db: Database,
        current_user: User,
) -> None:
    order = await OrderService(db, current_user).get(callback_data.id)
    await query.answer()
    if isinstance(query.message, Message):
        await show_order(order,
                         current_user=current_user,
                         message=query.message,
                         replace_text=True)


scene_registry.add(EditOrderScene)
router.callback_query.register(
    EditOrderScene.as_handler(), OrderCallbackData.filter(F.action == "edit"))


@router.callback_query(OrderCallbackData.filter(
    F.action.in_({"trash_ask", "delete_ask", "duplicate_ask"})))
async def order_trash_ask_callback_handler(query: CallbackQuery, callback_data: OrderCallbackData) -> None:
    match callback_data.action:
        case "trash_ask":
            action, text = "trash", "Вы уверены что хотите удалить заказ?"
        case "delete_ask":
            action, text = "delete", "Заказ будет удалён окончательно. Вы уверены?"
        case "duplicate_ask":
            action, text = "duplicate", "Будет создана копия заказа. Вы уверены?"
        case _:
            return
    await query.answer()
    if isinstance(query.message, Message):
        await query.message.edit_text(
            text, reply_markup=ok_cancel_kb(
                        ok_cb=OrderCallbackData(id=callback_data.id, action=action),
                        cancel_cb=OrderCallbackData(id=callback_data.id)))


@router.callback_query(OrderCallbackData.filter(F.action == "duplicate"))
async def order_duplicate_callback_handler(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        db: Database,
        current_user: User,
) -> None:
    service = OrderService(db, current_user)
    order = await service.get(callback_data.id)
    new_order = await service.new(OrderAdd(user_id=current_user.id,
                                           label=order.label,
                                           size=order.size,
                                           qty=order.qty))
    await query.answer()
    if isinstance(query.message, Message):
        await show_order(new_order, "Создана копия заказа",
                         current_user=current_user,
                         message=query.message,
                         replace_text=True)


@router.callback_query(OrderCallbackData.filter(F.action))
async def order_actions_callback_handler(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        db: Database,
        current_user: User,
) -> None:
    service = OrderService(db, current_user)
    order_id = callback_data.id
    notice, back = None, False
    match callback_data.action:
        case "submit":
            await service.submit(order_id)
            notice = "Заказ отправлен на проверку"
        case "return":
            await service.return_(order_id)
            notice = "Заказ возвращен на доработку"
        case "accept":
            await service.accept(order_id)
            notice = "Заказ взят в работу"
        case "reject":
            await service.reject(order_id)
            notice = "Заказ возвращён на доработку"
        case "done":
            await service.done(order_id)
            notice = "Заказ завершён"
        case "trash":
            await service.trash(order_id)
            notice, back = f"Заказ #{order_id} удалён", True
        case "restore":
            await service.restore(order_id)
            notice = "Заказ восстановлен"
        case "delete":
            await service.delete(order_id)
            notice, back = f"Заказ #{order_id} удален окончательно", True
        case "back" | _:
            back = True
    await query.answer()
    if isinstance(query.message, Message):
        if back:
            callback_data = OrdersCallbackData()
            params = callback_data.model_dump(exclude_none=True)
            if current_user.role < UserRole.AGENT:
                params["user_id"] = current_user.id
            result = await OrderService(db, current_user).get_many(OrderQueryPaged(**params))
            await show_orders(result,
                              callback_data,
                              notice,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)
        else:
            await show_order(await service.get(order_id),
                             notice,
                             current_user=current_user,
                             message=query.message,
                             replace_text=True)
