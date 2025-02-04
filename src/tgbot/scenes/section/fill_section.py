from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.tgbot.scenes.form import VISA_FIELDS
from src.tgbot.utils.fields import validate_field_input
from src.tgbot.views.common.field_input import show_field_input

"""
State data structure:
{
    "fill_section.section_id": section_id,
    "fill_section.section_step": section_step,
    "fill_section.data.{field_id}": value.
    ...
}
"""

class FillSectionScene(Scene, state="fill_section"):


    @on.message.enter()
    async def message_on_enter(
            self, message: Message, state: FSMContext, deps: Dependencies) -> None:
        state_data = await state.get_data()
        form_step = state_data.get("form.current_step", 0)
        section_step = state_data.get("section.current_step", 0)
        section = VISA_FIELDS[step]
        if section_step == 0:
            await message.answer(f"Раздел {form_step + 1}: {section.name}")
        try:
            field = section.fields[section_step]
            await show_field_input(field, message=message)
        except IndexError:
            data = state_data.get("section_data", {})
            await state.update_data(section_step=0, section_data={})
            await self.wizard.goto("fill_form")


    @on.callback_query.enter()
    async def callback_query_on_enter(
            self, query: CallbackQuery, state: FSMContext, step: int) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message, state, step)


    @on.message(F.text)
    async def process_input(self, message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        step = state_data.get("step")
        section_step = state_data.get("section_step", 0)
        section_data = state_data.get("section_data", {})
        if message.text:
            section = VISA_FIELDS[step]
            field = section.fields[section_step]
            await validate_field_input(field, message.text)
            section_data[field.id] = message.text
            section_step += 1
            await state.update_data(section_step=section_step, section_data=section_data)
            await self.wizard.retake(step=step)
