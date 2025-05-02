from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from core.entities.survey import FieldType, Others, Repeater, Section, YesNo
from core.exceptions import ValidationError
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from interfaces.tgbot.views.buttons import ALL
from interfaces.tgbot.views.surveys.field import show_all_options, show_field_input
from interfaces.tgbot.views.surveys.survey import SURVEY_RECHECK_TEXT, show_survey_done_message


class SurveyScene(Scene, state="survey"):

    @on.message.enter()
    async def message_on_enter(self,  # noqa: C901
                               message: Message,
                               state: FSMContext, *,
                               deps: TgBotDependencies,
                               survey_id: str | None = None) -> None:

        data = await state.get_data()

        if survey_id is not None:
            # Set defaults
            data["survey.id"] = survey_id
            data["survey.survey_step"] = 0
            data["survey.section_step"] = 0
            await state.set_data(data)

        # Show template depending on state data
        survey_id = data["survey.id"]
        survey_step = data["survey.survey_step"]
        section_step = data["survey.section_step"]

        form_service = deps.get_survey_service()
        survey = form_service.get_survey(survey_id)

        try:
            section = survey.sections[survey_step]
        except IndexError:
            await show_survey_done_message(message)
        else:

            # Show section title and save message id
            if section_step == 0 and data.get("survey_section.section_id", None) is None:
                _message = await message.answer(
                    f"<b>{survey_step + 1}. {section.name.upper()}</b>")
                data["survey.section_title_id"] = _message.message_id
                await state.set_data(data)

            if isinstance(section, Repeater):
                await self.wizard.goto("survey_repeater", repeater_id=section.id)

            elif isinstance(section, Section):
                try:
                    field = section.fields[section_step]
                except IndexError:
                    await self.wizard.goto("survey_section", section_id=section.id)
                else:

                    key = f"survey.data.{section.id}.{field.id}"
                    if key not in data:
                        if field.depends_on:
                            cond_field = form_service.get_field(field.depends_on)
                            cond_key = f"survey.data.{section.id}.{cond_field.id}"
                            cond_value = data.get(cond_key, YesNo.NO)
                            if cond_value == YesNo.YES or cond_value in Others:
                                await show_field_input(field, message=message)
                                return
                        else:
                            await show_field_input(field, message=message)
                            return

                    data["survey.section_step"] = section_step + 1
                    await state.set_data(data)
                    await self.wizard.retake()


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: TgBotDependencies,
                                      survey_id: str | None = None) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state,
                                        deps=deps,
                                        survey_id=survey_id)


    @on.callback_query(F.data)
    async def form_data_update_callback(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message) and query.data.startswith("survey:"):
                _, action = query.data.split(":")

                if action == "recheck":
                    await state.update_data({"survey.survey_step": 0,
                                             "survey.section_step": 0})
                    await query.message.edit_text(SURVEY_RECHECK_TEXT)
                    await self.wizard.retake()

                elif action == "save":
                    await state.update_data({"survey.completed": True})
                    await query.message.delete()
                    await self.wizard.goto("apply_visa")


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext, *,
                            deps: TgBotDependencies) -> None:

        if message.text:
            data = await state.get_data()
            survey_id = data["survey.id"]
            survey_step = data["survey.survey_step"]
            section_step = data["survey.section_step"]

            survey_service = deps.get_survey_service()
            survey = survey_service.get_survey(survey_id)
            try:
                section = survey.sections[survey_step]
                field = section.fields[section_step]
            except IndexError:
                return

            if field.type == FieldType.CHOICE and message.text == ALL:
                await show_all_options(field, message=message)
                return

            try:
                value = survey_service.format_and_validate_input(field, message.text)
            except ValidationError as error:
                await message.answer(f"❌ {error}")
                return

            data[f"survey.data.{section.id}.{field.id}"] = value
            data["survey.section_step"] = section_step + 1
            await state.set_data(data)
            await self.wizard.retake()
