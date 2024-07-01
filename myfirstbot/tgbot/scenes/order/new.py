from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message

from myfirstbot.entities.order import OrderAdd
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.scenes.order import ORDER_FIELDS
from myfirstbot.tgbot.utils.fields import validate_field_input
from myfirstbot.tgbot.views.common.field_input import show_field_input
from myfirstbot.tgbot.views.order.order import show_order


class NewOrderScene(Scene, state="new_order"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        step = (await state.get_data()).get("step", 0)
        if step == 0:
            await message.answer("Welcome to the wizard!")
        try:
            field = ORDER_FIELDS[step]
            await show_field_input(field, message=message)
        except IndexError:
            await self.wizard.exit()

    @on.message.exit()
    async def on_exit(
            self,
            message: Message,
            state: FSMContext,
            db: Database,
            current_user: User,
    ) -> None:
        order_data = (await state.get_data()).get("order", {})
        order_data["user_id"] = current_user.id
        order = await OrderService(db, current_user).new(OrderAdd(**order_data))
        await show_order(order,"Заказ успешно создан",
                         current_user=current_user,
                         message=message)
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
