from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
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
                               form_id: str) -> None:

        form = deps.forms.get_form(form_id)
        data = await state.get_data()
        data["form.form_id"] = form_id
        form_step = data.get("form.form_step", 0)
        section_step = data.get("form.section_step", 0)

        try:
            section = form.sections[form_step]
            await state.set_data(data)
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
                # Skip field if value is not empty
                if data.get(f"form.data.{section.id}.{field.id}", None) is not None:
                    section_step += 1
                    data["form.section_step"] = section_step
                    await state.set_data(data)
                    await self.wizard.retake(form_id=form_id)
                else:
                    await show_field_input(field, message=message)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      form_id: str) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state, deps,
                                        form_id=form_id)


    @on.callback_query(F.data)
    async def form_data_update_callback(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message) and query.data.startswith("form_checked:"):
            _, checked = query.data.split(":")
            if checked == "no":
                data = await state.get_data()
                form_id = data["form.form_id"]
                data["form.form_step"] = 0
                data["form.section_step"] = 0
                await state.set_data(data)
                await query.message.edit_text(FORM_RECHECK)
                await self.wizard.retake(form_id=form_id)
            elif checked == "yes":
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
            form = deps.forms.get_form(form_id)
            form_step = data.get("form.form_step", 0)
            section = form.sections[form_step]
            section_step = data.get("form.section_step", 0)
            field = section.fields[section_step]
            if message.text == ALL:
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
            await self.wizard.retake(form_id=form_id)
