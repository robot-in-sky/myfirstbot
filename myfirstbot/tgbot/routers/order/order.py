from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.callbacks import OrderCallbackData
from myfirstbot.tgbot.scenes import EditOrderScene, NewOrderScene
from myfirstbot.tgbot.views.common.ok_cancel import ok_cancel_kb
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.order.order import show_order

router = Router()
scene_registry = SceneRegistry(router)


scene_registry.add(NewOrderScene)
router.message.register(
    NewOrderScene.as_handler(), F.text == buttons.NEW_ORDER)


@router.callback_query(OrderCallbackData.filter(~F.action))
async def order_get_callback(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        db: Database,
        current_user: User,
) -> None:
    order = await OrderService(db, current_user).get(callback_data.id)
    await query.answer()
    await show_order(order,
                     current_user=current_user,
                     message=query.message)


scene_registry.add(EditOrderScene)
router.callback_query.register(
    EditOrderScene.as_handler(), OrderCallbackData.filter(F.action == "edit"))


@router.callback_query(OrderCallbackData.filter(F.action == "trash_ask"))
async def order_action_trash_callback(query: CallbackQuery, callback_data: OrderCallbackData) -> None:
    await query.answer()
    await query.message.edit_text(
        "Вы уверены что хотите удалить заказ?",
        reply_markup=ok_cancel_kb(
            ok_cb=OrderCallbackData(id=callback_data.id, action="trash"),
            cancel_cb=OrderCallbackData(id=callback_data.id)))


@router.callback_query(OrderCallbackData.filter(F.action))
async def order_actions_callback(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        db: Database,
        current_user: User,
) -> None:
    await query.answer()
    service = OrderService(db, current_user)
    order_id = callback_data.id
    notice, to_menu = None, False
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
            notice, to_menu = f"Заказ #{order_id} удалён", True
        case "restore":
            await service.restore(order_id)
            notice = "Заказ восстановлен"
        case "delete":
            await service.delete(order_id)
            notice, to_menu = f"Заказ #{order_id} удален окончательно", True
        case "to_menu":
            notice, to_menu = "Главное меню", True
        case _:
            return
    if to_menu:
        await query.message.answer(notice, reply_markup=main_menu_kb(current_user))
    else:
        await show_order(await service.get(order_id),
                         notice,
                         current_user=current_user,
                         message=query.message,
                         replace_text=True)
