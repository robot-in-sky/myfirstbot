from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.users import User
from src.entities.visas import AppFormQuery, AppFormQueryPaged
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.const import PER_PAGE_DEFAULT
from src.tgbot.views.menu import show_menu
from src.tgbot.views.visas.app_forms import show_app_form_filter, show_app_forms

SEARCH_TEXT = "Введите поисковую фразу"


class MyAppFormsScene(Scene, state="my_app_forms"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               current_user: User) -> None:

        data = await state.get_data()
        if isinstance(message, Message):
            service = deps.get_my_app_forms_service(current_user)
            params = sub_dict_by_prefix(data, prefix="query.")
            params["per_page"] = PER_PAGE_DEFAULT
            if data.get("state") == "filter":
                params = {k: params[k] for k in params if k not in {"status", "page", "per_page"}}
                # print("get_my_forms_count_by_status", params)
                query = AppFormQuery(**params)
                count_by_status = await service.get_my_forms_count_by_status(query)
                total_count = await service.get_my_forms_count(query)
                await show_app_form_filter(count_by_status,
                                           total_count,
                                           status=params.get("status"),
                                           search=params.get("search"),
                                           user_id=current_user.id,
                                           message=message,
                                           replace=True,
                                           current_user=current_user)
            else:
                if params.get("status") == "all":
                    params["status"] = None
                # print("get_my_forms", params)
                query = AppFormQueryPaged(**params)
                result = await service.get_my_forms(query)
                replace = True
                if data.get("message_id") is not None:
                    await message.chat.delete_message(data["message_id"])
                    data["message_id"] = None
                    await state.set_data(data)
                    replace = False
                await show_app_forms(result,
                                     status=params.get("status"),
                                     search=params.get("search"),
                                     user_id=current_user.id,
                                     message=message,
                                     replace=replace,
                                     current_user=current_user)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message, state, deps,
                                        current_user=current_user)


    @on.callback_query(F.data)
    async def app_forms_action_callback(self,
                                        query: CallbackQuery,
                                        state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            match query.data:
                case query.data if query.data.startswith("action:"):
                    _, action = query.data.split(":")
                    if action == "filter":
                        await state.update_data({"state": "filter"})
                        await self.wizard.retake()

                    elif action == "search":
                        data = await state.get_data()
                        if data.get("query.search") is not None:
                            data["query.search"] = None
                            data["state"] = None
                            await state.set_data(data)
                            await self.wizard.retake()
                        else:
                            await query.message.answer(SEARCH_TEXT)
                            data["state"] = "search"
                            data["message_id"] = query.message.message_id
                            await state.set_data(data)

                case query.data if query.data.startswith("page:"):
                    _, page = query.data.split(":")
                    await state.update_data({"query.page": page, "state": None})
                    await self.wizard.retake()

                case query.data if query.data.startswith("filter:status:"):
                    _, _, status = query.data.split(":")
                    await state.update_data({"query.status": status, "state": None})
                    await self.wizard.retake()

                case query.data if query.data.startswith("app_form:"):
                    _, id_ = query.data.split(":")
                    await state.update_data({"state": None})
                    await self.wizard.goto("my_app_form", id_=id_)

                case "back":
                    await state.update_data({"state": None})
                    await self.wizard.retake()


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext) -> None:
        if message.text:
            data = await state.get_data()
            if data.get("state") == "search":
                data["query.search"] = message.text
                data["state"] = None
                await state.set_data(data)
                await self.wizard.retake()
