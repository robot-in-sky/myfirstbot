from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, ForceReply, Message

from src.deps import Dependencies
from src.entities.choices import UserRole
from src.entities.user import User, UserQueryPaged
from src.services import UserService
from src.tgbot.callbacks import UserSearchCallbackData, UsersCallbackData
from src.tgbot.views.user.users import show_users


class SearchUserScene(Scene, state="search_user"):

    @on.callback_query.enter()
    async def on_enter_callback(
            self,
            query: CallbackQuery,
            state: FSMContext,
    ) -> None:
        if query.data is None:
            return
        callback_data = UserSearchCallbackData.unpack(query.data)
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
        if params.get("role"):
            params["role"] = UserRole(params["role"])
        result = await UserService(deps, current_user).get_many(UserQueryPaged(**params))
        callback_data = UsersCallbackData(**params)
        await message.chat.delete_message(data["message_id"])
        await show_users(result,
                         callback_data,
                         message=message)
        await state.set_data({})

    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        params = (await state.get_data()).get("params", {})
        if message.text:
            params["search"] = message.text
            await state.update_data(params=params)
            await self.wizard.exit()
