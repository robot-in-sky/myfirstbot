from typing import Any

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.entities.order import OrderUpdate
from src.entities.user import User
from src.repositories.utils import Database
from src.services import OrderService
from src.tgbot.callbacks import EditorCallbackData, OrderCallbackData
from src.tgbot.scenes.order import ORDER_FIELDS
from src.tgbot.utils.fields import validate_field_input
from src.tgbot.views.common.editor import editor_kb, editor_summary
from src.tgbot.views.common.field_input import show_field_input
from src.tgbot.views.order.order import show_order


async def show_order_editor(
        data: dict[str, Any],
        selected: str,
        *,
        message: Message,
        replace_text: bool = False,
) -> Message:
    text = f"<b>Заказ #{data['id']}</b> — Редактирование\n\n"
    text += editor_summary(ORDER_FIELDS, data, selected)
    keyboard = editor_kb()
    if replace_text:
        await message.edit_text(text, reply_markup=keyboard)
        return message
    return await message.answer(text, reply_markup=keyboard)


class EditOrderScene(Scene, state="edit_order"):

    @on.callback_query.enter()
    async def on_enter_callback(
            self,
            query: CallbackQuery,
            state: FSMContext,
            db: Database,
            current_user: User,
    ) -> None:
        if query.data is None:
            return
        order_id = OrderCallbackData.unpack(query.data).id
        order_data = (await OrderService(db, current_user).get(order_id)).model_dump()
        field_ids = ["id"] + [f.id for f in ORDER_FIELDS]
        order_data = {id_: order_data[id_] for id_ in field_ids}
        idx = 0
        await query.answer()
        if isinstance(query.message, Message):
            message = await show_order_editor(order_data,
                                              ORDER_FIELDS[idx].id,
                                              message=query.message,
                                              replace_text=True)

            await state.set_data({"order_original": order_data,
                                  "order_updated": order_data,
                                  "selector_idx": idx,
                                  "expect_input": False,
                                  "message_id": message.message_id})

    @on.callback_query(EditorCallbackData.filter())
    async def editor_actions_callback(  # noqa: PLR0913
            self,
            query: CallbackQuery,
            callback_data: OrderCallbackData,
            state: FSMContext,
            db: Database,
            current_user: User,
    ) -> None:
        data = await state.get_data()
        order_data, idx = data["order_updated"], data["selector_idx"]
        await query.answer()
        if isinstance(query.message, Message):
            match callback_data.action:
                case "up" | "down" as action:
                    last_idx = len(ORDER_FIELDS) - 1
                    prev_idx = idx - 1 if idx > 0 else last_idx
                    next_idx = idx + 1 if idx < last_idx else 0
                    idx = prev_idx if action == "up" else next_idx
                    field = ORDER_FIELDS[idx]
                    await show_order_editor(order_data, field.id,
                                            message=query.message,
                                            replace_text=True)
                    await state.update_data(selector_idx=idx)

                case "edit":
                    field = ORDER_FIELDS[idx]
                    value = order_data.get(field.id)
                    await show_field_input(field, value, message=query.message)
                    await state.update_data(expect_input=True)

                case "return":
                    field = ORDER_FIELDS[idx]
                    if order_data[field.id] != data["order_original"].get(field.id):
                        order_data[field.id] = data["order_original"].get(field.id)
                        await show_order_editor(order_data, field.id,
                                                message=query.message,
                                                replace_text=True)
                        await state.update_data(order_updated=order_data)

                case "save" | "cancel" | _ as action:
                    service = OrderService(db, current_user)
                    if action == "save":
                        if order_data != data["order_original"]:
                            update = {f.id: order_data[f.id] for f in ORDER_FIELDS}
                            order = await service.update(order_data["id"], OrderUpdate(**update))
                            notice = "Заказ успешно обновлён"
                        else:
                            order = await service.get(order_data["id"])
                            notice = "Данные заказа не изменились"
                    else:
                        order = await service.get(order_data["id"])
                        notice = None
                    await show_order(order, notice,
                                     current_user=current_user,
                                     message=query.message,
                                     replace_text=True)
                    await self.wizard.exit()

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        if data["expect_input"] and message.text:
            order_data, idx = data["order_updated"], data["selector_idx"]
            field = ORDER_FIELDS[idx]
            await validate_field_input(field, message.text)
            order_data[field.id] = message.text
            await message.answer("Значение изменено", reply_markup=ReplyKeyboardRemove())
            await message.chat.delete_message(data["message_id"])
            message = await show_order_editor(order_data, field.id, message=message)
            await state.update_data(order_updated=order_data,
                                    expect_input=False,
                                    message_id=message.message_id)
