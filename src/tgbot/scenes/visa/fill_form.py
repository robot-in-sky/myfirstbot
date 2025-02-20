from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.form import FieldType, YesNo
from src.exceptions import ValidationError
from src.tgbot.views.buttons import ALL
from src.tgbot.views.form.field import show_all_options, show_field_input
from src.tgbot.views.form.form import FORM_RECHECK, show_form_done_message

"""
    "form.form_id": form_id,
    "form.form_step": form_step,
    "form.section_step": section_step,
    "form.data.{section_id}.{field_id}": value
    ...
"""

class FillFormScene(Scene, state="fill_form"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               form_id: str | None = None) -> None:

        data = await state.get_data()

        if form_id is not None:
            # Set defaults
            data["form.form_id"] = form_id
            data["form.form_step"] = 0
            data["form.section_step"] = 0
            await state.set_data(data)

        # Show template depending on state data
        form_id = data["form.form_id"]
        form_step = data["form.form_step"]
        section_step = data["form.section_step"]

        form = deps.forms.get_form(form_id)
        try:
            section = form.sections[form_step]
        except IndexError:
            await show_form_done_message(message)
        else:

            if section_step == 0:
                await message.answer(
                    f"<b>{form_step + 1}. {section.name}</b>")
            try:
                field = section.fields[section_step]
            except IndexError:
                await self.wizard.goto("edit_section", section_id=section.id)
            else:

                key = f"form.data.{section.id}.{field.id}"
                if key not in data:
                    if field.depends_on:
                        cond_field = deps.forms.get_field(field.depends_on)
                        cond_key = f"form.data.{section.id}.{cond_field.id}"
                        cond_value = data.get(cond_key, YesNo.NO)
                        if cond_value == YesNo.YES:
                            await show_field_input(field, message=message)
                            return
                    else:
                        await show_field_input(field, message=message)
                        return

                data["form.section_step"] = section_step + 1
                await state.set_data(data)
                await self.wizard.retake()


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      form_id: str | None = None) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state, deps,
                                        form_id=form_id)


    @on.callback_query(F.data)
    async def form_data_update_callback(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message) and query.data.startswith("form:"):
                _, action = query.data.split(":")

                if action == "recheck":
                    await state.update_data({"form.form_step": 0,
                                             "form.section_step": 0})
                    await query.message.edit_text(FORM_RECHECK)
                    await self.wizard.retake()

                elif action == "save":
                    await query.message.delete()
                    await self.wizard.goto("apply_visa")


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext,
                            deps: Dependencies) -> None:

        if message.text:
            data = await state.get_data()
            form_id = data["form.form_id"]
            form_step = data["form.form_step"]
            section_step = data["form.section_step"]

            form = deps.forms.get_form(form_id)
            section = form.sections[form_step]
            field = section.fields[section_step]

            if field.type == FieldType.CHOICE and message.text == ALL:
                await show_all_options(field, message=message)
                return

            try:
                value = deps.forms.validate_input(field, message.text)
            except ValidationError as error:
                await message.answer(str(error))
                return

            data[f"form.data.{section.id}.{field.id}"] = value
            data["form.section_step"] = section_step + 1
            await state.set_data(data)
            await self.wizard.retake()
