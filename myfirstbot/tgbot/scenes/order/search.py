from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, ForceReply, Message

from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.callbacks import OrderSearchCallbackData, OrdersCallbackData
from myfirstbot.tgbot.views.order.orders import show_orders


class SearchOrderScene(Scene, state="search_order"):

    @on.callback_query.enter()
    async def on_enter_callback(
            self,
            query: CallbackQuery,
            state: FSMContext,
    ) -> None:
        if query.data is None:
            return
        callback_data = OrderSearchCallbackData.unpack(query.data)
        params = callback_data.model_dump(exclude_none=True, exclude={"page"})
        await query.answer()
        if isinstance(query.message, Message):
            await query.message.answer("Введите поисковую фразу",
                                        reply_markup=ForceReply(force_reply=True))
            await state.set_data({"params": params,
                                  "message_id": query.message.message_id})

    @on.message.exit()
    async def on_exit(
            self,
            message: Message,
            state: FSMContext,
            db: Database,
            current_user: User,
    ) -> None:
        data = await state.get_data()
        params = data.get("params", {})
        if current_user.role < UserRole.AGENT:
            params["user_id"] = current_user.id
        if params.get("status"):
            params["status"] = OrderStatus(params["status"])
        result = await OrderService(db, current_user).get_all(**params)
        callback_data = OrdersCallbackData(**params)
        await message.chat.delete_message(data["message_id"])
        await show_orders(result,
                          callback_data,
                          current_user=current_user,
                          message=message)
        await state.set_data({})

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        params = (await state.get_data()).get("params", {})
        if message.text:
            params["s"] = message.text
            await state.update_data(params=params)
            await self.wizard.exit()
