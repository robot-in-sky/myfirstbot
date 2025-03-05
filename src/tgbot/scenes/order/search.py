from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, ForceReply, Message

from src.deps import Dependencies
from src.entities.order import OrderQueryPaged, OrderStatus
from src.entities.users import User, UserRole
from src.tgbot.callbacks import OrderSearchCallbackData, OrdersCallbackData
from src.tgbot.views.visas.app_forms import show_orders


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
            deps: Dependencies,
            current_user: User,
    ) -> None:
        data = await state.get_data()
        params = data.get("params", {})
        if current_user.role < UserRole.AGENT:
            params["user_id"] = current_user.id
        if params.get("status"):
            params["status"] = OrderStatus(params["status"])
        result = await deps.orders(current_user).get_many(OrderQueryPaged(**params))
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
            params["search"] = message.text
            await state.update_data(params=params)
            await self.wizard.exit()
