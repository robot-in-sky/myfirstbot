import asyncio
from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from interfaces.tgbot.tgbot_deps import TgBotDependencies
from core.entities.forms import FieldType, Repeater, YesNo
from core.entities.users import User
from core.entities.visas import AppFormUpdate
from core.exceptions import ValidationError
from interfaces.tgbot.utils.helpers import remove_keys_by_prefix, sub_dict_by_prefix
from interfaces.tgbot.views.buttons import ALL
from interfaces.tgbot.views.forms.field import show_all_options, show_field_input
from interfaces.tgbot.views.forms.repeater import (
    show_repeater,
    show_repeater_completed,
    show_repeater_description,
)
from interfaces.tgbot.views.forms.section import show_check_section


class VisaFormRepeaterScene(Scene, state="visa_form_repeater"):

    @on.message.enter()
    async def message_on_enter(self,  # noqa: PLR0913
                               message: Message,
                               state: FSMContext, *,
                               deps: TgBotDependencies,
                               repeater_id: str | None = None,
                               replace: bool = False) -> None:

        data = await state.get_data()

        if repeater_id is not None:
            # Set defaults
            data["repeater.id"] = repeater_id
            data["repeater.item.step"] = 0
            await state.set_data(data)

        repeater_id = data["repeater.id"]
        form_service = deps.get_forms_service()
        repeater = form_service.get_section(repeater_id)
        if not isinstance(repeater, Repeater):
            return

        step_key = f"form.data.{repeater_id}.step"

        if step_key not in data:
            field = repeater.condition_field
            await show_field_input(field, message=message, replace=replace)
            return

        step = data[step_key]

        # Check modified or not
        title_msg_id = data.get("form.section_title_id", -1)
        section_modified = message.message_id > title_msg_id

        # If condition value is "No"
        if step == -1:
            if section_modified:
                await show_check_section(message=message)
            await show_repeater(repeater, data=[], message=message)
            return

        # Internal step
        item_step_key = f"form.data.{repeater_id}.item_step"
        item_step = data.get(item_step_key, 0)

        if step == item_step == 0:
            await show_repeater_description(repeater, message=message, replace=replace)
            replace = False

        try:
            field = repeater.repeater_fields[item_step]
        except IndexError:
            repeater_data = [sub_dict_by_prefix(data, prefix=f"form.data.{repeater_id}.{step_}.")
                                 for step_ in range(step + 1)]
            if section_modified:
                await show_check_section(message=message)
            await show_repeater(repeater, repeater_data, message=message)
        else:
            await show_field_input(field, message=message, replace=replace)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,  # noqa: PLR0913
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: TgBotDependencies,
                                      repeater_id: str | None = None,
                                      replace: bool = False) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state,
                                        deps=deps,
                                        repeater_id=repeater_id,
                                        replace=replace)


    @on.callback_query(F.data)
    async def repeater_action_callback(self,
                                       query: CallbackQuery,
                                       state: FSMContext, *,
                                       deps: TgBotDependencies,
                                       current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message) and query.data.startswith("repeater:"):
                _, action = query.data.split(":")
                data = await state.get_data()
                repeater_id = data["repeater.id"]
                match action:

                    case "add":
                        step_key = f"form.data.{repeater_id}.step"
                        data[step_key] = data[step_key] + 1
                        item_step_key = f"form.data.{repeater_id}.item_step"
                        data[item_step_key] = 0
                        await state.set_data(data)
                        await self.wizard.retake(replace=True)

                    case "reset":
                        # Reset data to default
                        data = remove_keys_by_prefix(data, prefix=f"form.data.{repeater_id}.")
                        await state.set_data(data)
                        await self.wizard.retake(repeater_id=repeater_id, replace=True)

                    case "confirm":
                        # Remove keyboard and show confirmation
                        await query.message.edit_reply_markup(reply_markup=None)
                        await show_repeater_completed(query.message)
                        await asyncio.sleep(0.3)
                        # Switch form step
                        data["form.form_step"] = data["form.form_step"] + 1
                        data["form.section_step"] = 0
                        await state.set_data(data)
                        # Autosave
                        service = deps.get_my_app_forms_service(current_user)
                        id_ = UUID(data["visa.app_form_id"])
                        await service.update_form(id_, AppFormUpdate(data=data))
                        # Go back to the form scene
                        await self.wizard.goto("visa_form")


    @on.message(F.text)
    async def process_input(self,  # noqa: PLR0912
                            message: Message,
                            state: FSMContext, *,
                            deps: TgBotDependencies) -> None:

        if message.text:
            data = await state.get_data()
            repeater_id = data["repeater.id"]
            form_service = deps.get_forms_service()
            repeater = form_service.get_section(repeater_id)
            if not isinstance(repeater, Repeater):
                return

            step_key = f"form.data.{repeater_id}.step"
            item_step_key = f"form.data.{repeater_id}.item_step"
            item_step = data.get(item_step_key, 0)

            if step_key not in data:
                field = repeater.condition_field
            else:
                try:
                    field = repeater.repeater_fields[item_step]
                except IndexError:
                    return

            if field.type == FieldType.CHOICE and message.text == ALL:
                await show_all_options(field, message=message)
                return

            try:
                value = form_service.format_and_validate_input(field, message.text)
            except ValidationError as error:
                await message.answer(str(error))
                return

            if step_key not in data:
                if value == YesNo.YES:
                    data[step_key] = 0
                else:
                    data[step_key] = -1
            else:
                step = data[step_key]
                data[f"form.data.{repeater_id}.{step}.{field.id}"] = value
                data[item_step_key] = item_step + 1

            await state.set_data(data)
            await self.wizard.retake()

