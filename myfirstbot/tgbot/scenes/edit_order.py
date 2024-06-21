from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.order import OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.scenes.utils.order_fields import order_fields
from myfirstbot.tgbot.views.orders.order import order_actions_kb, order_summary


class EditOrderScene(Scene, state="edit_order"):

    @on.callback_query.enter()
    async def on_callback_query_enter(  # noqa: PLR0913
            self,
            query: CallbackQuery,
            state: FSMContext,
            db: Database,
            user: User,
            *,
            editor_action: str | None = None,
    ) -> None:
        await query.answer()
        if editor_action is None:
            order_id = int(query.data.split(":")[-1])
            order = (await OrderService(db, user).get(order_id)).model_dump()
            selected = order_fields.ids[0]
            field_ids = ["id", *order_fields.ids]
            order = {id_: order[id_] for id_ in field_ids}
            editor_message = await order_fields.show_editor(
                    order, selected, message=query.message, replace_text=True)
            await state.set_data({
                "order": order,
                "selected": selected,
                "editor_id": editor_message.message_id,
            })
        else:
            data = await state.get_data()
            order, selected = data["order"], data["selected"]
            idx = order_fields.index_by_id(selected)
            last_idx = len(order_fields.ids) - 1
            match editor_action:
                case "up":
                    idx = idx - 1 if idx > 0 else last_idx
                    selected = order_fields.ids[idx]
                    await order_fields.show_editor(
                        order, selected, message=query.message, replace_text=True)
                    await state.update_data(selected=selected)
                case "down":
                    idx = idx + 1 if idx < last_idx else 0
                    selected = order_fields.ids[idx]
                    await order_fields.show_editor(
                        order, selected, message=query.message, replace_text=True)
                    await state.update_data(selected=selected)
                case "edit":
                    await order_fields.show_input(selected, message=query.message)

    @on.message.enter()
    async def on_message_enter(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        await message.chat.delete_message(data["editor_id"])
        editor_message = await order_fields.show_editor(
            data["order"], data["selected"], message=message)
        await state.update_data(editor_id=editor_message.message_id)

    @on.callback_query.exit()
    async def on_callback_query_exit(  # noqa: PLR0913
            self,
            query: CallbackQuery,
            state: FSMContext,
            db: Database,
            user: User,
            *,
            editor_action: str | None = None,
    ) -> None:
        data = (await state.get_data()).get("order", {})
        service = OrderService(db, user)
        match editor_action:
            case "save":
                field_ids = order_fields.ids
                update = {id_: data[id_] for id_ in field_ids}
                order = await service.update(data["id"], OrderUpdate(**update))
                notice = "<i>Заказ успешно обновлён</i>\n\n"
            case "cancel":
                order = await service.get(data["id"])
                notice = ""
            case _:
                return
        await query.answer()
        await query.message.edit_text(
            notice + order_summary(order, user),
            reply_markup=order_actions_kb(order, user),
        )
        await state.set_data({})

    @on.callback_query(F.data)
    async def button_callback(self, query: CallbackQuery) -> None:
        match query.data:
            case "editor_up":
                await self.wizard.retake(editor_action="up")
            case "editor_down":
                await self.wizard.retake(editor_action="down")
            case "editor_edit":
                await self.wizard.retake(editor_action="edit")
            case "editor_save":
                await self.wizard.exit(editor_action="save")
            case "editor_cancel":
                await self.wizard.exit(editor_action="cancel")

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        order, selected = data["order"], data["selected"]
        order[selected] = message.text
        await order_fields.validate_input(selected, message.text)
        await state.update_data(order=order)
        await self.wizard.retake()
