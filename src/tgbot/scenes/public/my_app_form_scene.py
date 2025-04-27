from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.users import User
from src.tgbot.views.keyboards import yes_no_kb
from src.tgbot.views.visas.app_form import show_app_form

TRASH_APP_FORM_TEXT = "Вы действительно хотите удалить заявку?"


class MyAppFormScene(Scene, state="my_app_form"):

    @on.message.enter()
    async def message_on_enter(self,  # noqa: PLR0913
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               current_user: User,
                               id_: str | None = None,
                               back: bool = True) -> None:

        data = await state.get_data()
        if id_ is not None:
            # Set defaults
            data["id"] = id_
            data["back"] = back
            data["state"] = None
            await state.set_data(data)

        if isinstance(message, Message):
            service = deps.get_my_app_forms_service(current_user)
            if data.get("id") and data.get("back") is not None:
                app_form = await service.get_form(UUID(data["id"]))
                await show_app_form(app_form,
                                    message=message,
                                    replace=back,
                                    back=data["back"],
                                    current_user=current_user)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,  # noqa: PLR0913
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      current_user: User,
                                      id_: str | None = None,
                                      back: bool = True) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message, state, deps,
                                        current_user=current_user,
                                        id_=id_, back=back)


    @on.callback_query(F.data)
    async def app_forms_action_callback(self,
                                        query: CallbackQuery,
                                        state: FSMContext, *,
                                        deps: Dependencies,
                                        current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            data = await state.get_data()
            service = deps.get_my_app_forms_service(current_user)
            match query.data:
                case query.data if query.data.startswith("action:"):
                    _, action = query.data.split(":")
                    if data.get("id"):
                        match action:
                            case "trash_ask":
                                await state.update_data({"state": "trash_ask"})
                                await query.message.edit_text(
                                    TRASH_APP_FORM_TEXT,
                                    reply_markup=yes_no_kb())
                            case "continue":
                                app_form = await service.get_form(UUID(data["id"]))
                                data = app_form.data
                                await state.set_data(data)
                                await self.wizard.goto("apply_visa")

                case "back":
                    await state.update_data({"id": None, "back": None})
                    await self.wizard.back()

                # case "to_menu":
                #     await state.clear()
                #     await self.wizard.exit()
                #     await show_menu(message=query.message,
                #                     current_user=current_user,
                #                     replace=True)

                case _:
                    if data.get("id") and data.get("state") == "trash_ask":
                        match query.data:
                            case "yes":
                                await service.trash_form(UUID(data["id"]))
                                await state.update_data({"id": None, "state": None})
                                await self.wizard.goto("my_app_forms")
                            case "no":
                                await state.update_data({"state": None})
                                await self.wizard.retake()
