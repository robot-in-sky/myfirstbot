from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.order import OrderAdd
from src.entities.user import User
from src.services import OrderService
from src.tgbot.scenes.order import ORDER_FIELDS
from src.tgbot.utils.fields import validate_field_input
from src.tgbot.views.common.field_input import show_field_input
from src.tgbot.views.order.order import show_order

WELCOME_TEXT = "Введите данные заказа"

class NewOrderScene(Scene, state="new_order"):

    @on.message.enter()
    async def message_on_enter(self, message: Message, state: FSMContext) -> None:
        step = (await state.get_data()).get("step", 0)
        if step == 0:
            await message.answer(WELCOME_TEXT)
        try:
            field = ORDER_FIELDS[step]
            await show_field_input(field, message=message)
        except IndexError:
            await self.wizard.exit()

    @on.callback_query.enter()
    async def callback_query_on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        step = (await state.get_data()).get("step", 0)
        await query.answer()
        if isinstance(query.message, Message):
            if step == 0:
                await query.message.answer(WELCOME_TEXT)
            try:
                field = ORDER_FIELDS[step]
                await show_field_input(field, message=query.message)
            except IndexError:
                await self.wizard.exit()

    @on.message.exit()
    async def on_exit(
            self,
            message: Message,
            state: FSMContext,
            deps: Dependencies,
            current_user: User,
    ) -> None:
        order_data = (await state.get_data()).get("order", {})
        order_data["user_id"] = current_user.id
        order = await OrderService(deps, current_user).new(OrderAdd(**order_data))
        await show_order(order,"Заказ успешно создан",
                         current_user=current_user,
                         message=message,
                         to_menu=True)
        await state.set_data({})

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data.get("step", 0)
        order_data = data.get("order", {})
        if message.text:
            field = ORDER_FIELDS[step]
            await validate_field_input(field, message.text)
            order_data[field.id] = message.text
            await state.update_data(order=order_data, step=step + 1)
            await self.wizard.retake()
