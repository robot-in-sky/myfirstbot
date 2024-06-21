from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.order import OrderAdd
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.scenes.utils.order_fields import order_fields
from myfirstbot.tgbot.views.orders.order import order_actions_kb, order_summary


class NewOrderScene(Scene, state="new_order"):

    @on.callback_query.enter()
    async def on_callback_query_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        await self.on_message_enter(query.message, state)

    @on.message.enter()
    async def on_message_enter(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data.get("step", 0)
        if step == 0:
            await message.answer("Welcome to the wizard!")
        if field_id := order_fields.id_by_index(step):
            await order_fields.show_input(field_id, message)
        else:
            await self.wizard.exit()

    @on.message.exit()
    async def on_message_exit(
            self,
            message: Message,
            state: FSMContext,
            db: Database,
            user: User,
    ) -> None:
        data = await state.get_data()
        order_data = data.get("order", {})
        order_data["user_id"] = user.id
        order = await OrderService(db, user).new(OrderAdd(**order_data))
        await message.answer(
            ("<i>Заказ успешно создан.</i>\n"
             "<i>Проверьте данные:</i>\n\n" +
             order_summary(order, user)),
            reply_markup=order_actions_kb(order, user),
        )
        await state.set_data({})

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data.get("step", 0)
        order = data.get("order", {})
        field_id = order_fields.id_by_index(step)
        order[field_id] = message.text
        await order_fields.validate_input(field_id, message.text)
        await state.update_data(order=order, step=step + 1)
        await self.wizard.retake()
