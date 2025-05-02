import asyncio
from uuid import UUID

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from core.entities.survey import FieldType, Others, Section, YesNo
from core.entities.users import User
from core.entities.visas import AppFormUpdate
from core.exceptions import ValidationError
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from interfaces.tgbot.utils.helpers import sub_dict_by_prefix
from interfaces.tgbot.views.buttons import ALL
from interfaces.tgbot.views.surveys.field import show_all_options, show_field_input
from interfaces.tgbot.views.surveys.section import (
    show_check_section,
    show_section,
    show_section_completed,
    show_section_fields,
)


class SurveySectionScene(Scene, state="survey_section"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext, *,
                               deps: TgBotDependencies,
                               section_id: str | None = None) -> None:

        data = await state.get_data()
        if section_id is not None:
            # Set defaults
            data["survey_section.id"] = section_id
            data["survey_section.field_id"] = None
            await state.set_data(data)

        section_id = data["survey_section.id"]
        field_id = data["survey_section.field_id"]
        form_service = deps.get_survey_service()

        if field_id is None:
            section = form_service.get_section(section_id)
            if isinstance(section, Section):
                section_data = sub_dict_by_prefix(data, prefix=f"survey.data.{section_id}.")
                title_msg_id = data.get("survey.section_title_id", -1)
                section_modified = message.message_id > title_msg_id
                if section_modified:
                    await show_check_section(message=message)
                await show_section(section, section_data, message=message)
        else:
            field = form_service.get_field(field_id)
            value = data.get(f"survey.data.{section_id}.{field_id}", None)

            if field.depends_on:
                _field = form_service.get_field(field.depends_on)
                _value = data.get(f"survey.data.{section_id}.{_field.id}", None)
                if _field.hidden or _value == YesNo.NO:
                    data["survey_section.field_id"] = _field.id
                    await state.set_data(data)
                    await self.wizard.retake()
                    return

            await show_field_input(field, value, message=message, replace=True)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: TgBotDependencies,
                                      section_id: str | None = None) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state,
                                        deps=deps,
                                        section_id=section_id)


    @on.callback_query(F.data)
    async def section_actions_callback(self,
                                       query: CallbackQuery,
                                       state: FSMContext, *,
                                       deps: TgBotDependencies,
                                       current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):

            if query.data.startswith("section:"):
                _, action = query.data.split(":")
                data = await state.get_data()
                match action:

                    case "confirm":
                        # Remove section keyboard
                        await query.message.edit_reply_markup(reply_markup=None)
                        await show_section_completed(query.message)
                        await asyncio.sleep(0.3)
                        data["survey_section.id"] = None
                        # Switch form step
                        data["survey.survey_step"] = data["survey.survey_step"] + 1
                        data["survey.section_step"] = 0
                        await state.set_data(data)
                        # Autosave
                        service = deps.get_my_app_forms_service(current_user)
                        id_ = UUID(data["visa.app_form_id"])
                        await service.update_form(id_, AppFormUpdate(data=data))
                        # Go back to form scene
                        await self.wizard.goto("survey")

                    case "edit":
                        section_id = data["survey_section.id"]
                        form_service = deps.get_survey_service()
                        section = form_service.get_section(section_id)
                        if isinstance(section, Section):
                            await show_section_fields(section, message=query.message)

            elif query.data.startswith("field:"):
                _, field_id = query.data.split(":")
                await state.update_data({"survey_section.field_id": field_id})
                await self.wizard.retake()


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext, *,
                            deps: TgBotDependencies) -> None:

        if message.text:
            data = await state.get_data()
            section_id = data["survey_section.id"]
            field_id = data["survey_section.field_id"]
            survey_service = deps.get_survey_service()
            field = survey_service.get_field(field_id)

            if field.type == FieldType.CHOICE and message.text == ALL:
                await show_all_options(field, message=message)
                return

            try:
                value = survey_service.format_and_validate_input(field, message.text)
            except ValidationError as error:
                await message.answer(f"❌ {error}")
                return

            key = f"survey.data.{section_id}.{field.id}"
            data[key] = value
            data["survey_section.field_id"] = None

            if field.type == FieldType.CHOICE:
                section = survey_service.get_section(section_id)
                if isinstance(section, Section):
                    dep_fields = False
                    for f in section.fields:
                        # Clear values of all dependable fields
                        if f.depends_on == field.id:
                            dep_fields = True
                            _key = f"survey.data.{section_id}.{f.id}"
                            if _key in data:
                                del data[_key]

                    if dep_fields and (value == YesNo.YES or value in Others):
                        # Go to refill all empty fields
                        data["survey.section_step"] = 0
                        await state.set_data(data)
                        await self.wizard.goto("survey")
                        return

            await state.set_data(data)
            await self.wizard.retake()

