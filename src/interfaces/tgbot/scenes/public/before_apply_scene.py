from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from core.entities.users import User
from core.entities.visas import AppFormQuery, AppFormQueryPaged, AppFormStatus
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from interfaces.tgbot.views.visas.before_apply import show_use_completed_step, show_use_saved_step


class BeforeApplyScene(Scene, state="before_apply"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext, *,
                               deps: TgBotDependencies,
                               current_user: User) -> None:

        data = await state.get_data()
        service = deps.get_my_app_forms_service(current_user)

        draft_count = await service.get_my_forms_count(
            AppFormQuery(status=AppFormStatus.DRAFT))
        completed_count = await service.get_my_forms_count(
            AppFormQuery(status=AppFormStatus.COMPLETED))

        if draft_count > 0 and data.get("use_saved") is None:
            await show_use_saved_step(message=message)

        elif data.get("use_saved"):
            if draft_count == 1:
                my_forms = await service.get_my_forms(
                                            AppFormQueryPaged(status=AppFormStatus.DRAFT))
                first_form = my_forms.items[0]
                await self.wizard.goto("my_app_form",
                                       id_=str(first_form.id),
                                       back=False)
            else:
                data["query.status"] = AppFormStatus.DRAFT
                await state.set_data(data)
                await self.wizard.goto("my_app_forms")

        elif completed_count > 0 and data.get("use_completed") is None:
            await show_use_completed_step(message=message)

        elif data.get("use_completed"):
            data["query.status"] = AppFormStatus.COMPLETED
            await state.set_data(data)
            await self.wizard.goto("my_app_forms")

        else:
            await self.wizard.goto("apply_visa")


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: TgBotDependencies,
                                      current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(message=query.message,
                                        state=state,
                                        deps=deps,
                                        current_user=current_user)

    @on.callback_query(F.data)
    async def app_forms_action_callback(self,
                                        query: CallbackQuery,
                                        state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message):

            data = await state.get_data()
            if data.get("use_saved") is None:
                if query.data == "yes":
                    data["use_saved"] = True
                else:
                    data["use_saved"] = False

            elif data.get("use_completed"):
                if query.data == "yes":
                    data["use_completed"] = True
                else:
                    data["use_completed"] = False

            await state.set_data(data)
            await self.wizard.retake()
