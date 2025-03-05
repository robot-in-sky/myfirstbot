from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.order import OrderAdd, OrderQueryPaged
from src.entities.users import User, UserRole
from src.tgbot.callbacks import OrderCallbackData, OrdersCallbackData
from src.tgbot.scenes import EditOrderScene, NewOrderScene
from src.tgbot.views import buttons
from src.tgbot.views.common.ok_cancel import ok_cancel_kb
from src.tgbot.views.visas.app_form import show_order
from src.tgbot.views.visas.app_forms import show_orders

router = Router()
scene_registry = SceneRegistry(router)


scene_registry.add(NewOrderScene)
router.message.register(
    NewOrderScene.as_handler(), F.text == buttons.APPLY_VISA)
router.callback_query.register(
    NewOrderScene.as_handler(), F.data == "new_order")


@router.callback_query(OrderCallbackData.filter(~F.action))
async def order_callback_handler(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    visa_forms = deps.get_my_app_form_service(current_user)
    order = await visa_forms.get_form(callback_data.id)
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
async def order_ask_callback_handler(query: CallbackQuery, callback_data: OrderCallbackData) -> None:
    match callback_data.action:
        case "trash_ask":
            action, text = "trash", "Вы уверены что хотите удалить анкету?"
        case "delete_ask":
            action, text = "delete", "Анкета будет удалена окончательно. Вы уверены?"
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


@router.callback_query(OrderCallbackData.filter(F.action))
async def order_action_callback_handler(
        query: CallbackQuery,
        callback_data: OrderCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    visa_forms = deps.get_my_app_form_service(current_user)
    form_id = callback_data.id
    notice, back = None, False
    match callback_data.action:
        case "submit":
            await visa_forms.submit_form(form_id)
            notice = "Заказ отправлен на проверку"
        case "return":
            await visa_forms.return_form(form_id)
            notice = "Заказ возвращен на доработку"
        case "trash":
            await visa_forms.trash_form(form_id)
            notice, back = f"Заказ #{form_id} удалён", True
        case "back" | _:
            back = True
    await query.answer()
    if isinstance(query.message, Message):
        if back:
            callback_data = OrdersCallbackData()
            params = callback_data.model_dump(exclude_none=True)
            if current_user.role < UserRole.AGENT:
                params["user_id"] = current_user.id
            result = visa_forms.get_my_forms(OrderQueryPaged(**params))
            await show_orders(result,
                              callback_data,
                              notice,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)
        else:
            await show_order(await orders.get(order_id),
                             notice,
                             current_user=current_user,
                             message=query.message,
                             replace_text=True)
