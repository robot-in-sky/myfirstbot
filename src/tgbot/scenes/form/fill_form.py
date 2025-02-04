from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.tgbot.utils.fields import validate_field_input
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.form.field import show_field_input
from src.tgbot.views.form.section import show_section

"""
    "form.form_id": form_id,
    "form.form_step": form_step,
    "form.section_step": section_step,
    "form.data.{section_id}.{field_id}": value
    ...
"""


WELCOME_TEXT = "Пожалуйста, заполните анкету"

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

        if form_step == section_step == 0:
            await message.answer(WELCOME_TEXT)

        try:
            section = form.sections[form_step]
        except IndexError:
            await self.wizard.goto("apply_visa")
        else:

            if section_step == 0:
                await message.answer(
                    f"<b>Шаг {form_step + 1}/{len(form.sections)}: {section.name}</b>")

            try:
                field = section.fields[section_step]
            except IndexError:
                # section_data = sub_dict_by_prefix(data, prefix=f"form.data.{section.id}")
                # await show_section(section, section_data)
                data["form.form_step"] = form_step + 1
                data["form.section_step"] = 0
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


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext,
                            deps: Dependencies) -> None:
        data = await state.get_data()
        form_id = data["form.form_id"]
        form_step = data.get("form.form_step", 0)
        section_step = data.get("form.section_step", 0)
        if message.text:
            form = deps.forms.get_form(form_id)
            section = form.sections[form_step]
            field = section.fields[section_step]
            await validate_field_input(field, message.text)
            field_key = f"form.data.{section.id}.{field.id}"
            data[field_key] = message.text
            data["form.section_step"] = section_step + 1
            await state.set_data(data)
            await self.wizard.retake(form_id=form_id)
