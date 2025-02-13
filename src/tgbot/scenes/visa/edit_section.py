import asyncio

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.exceptions import ValidationError
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.buttons import ALL
from src.tgbot.views.form.field import show_all_options, show_field_input
from src.tgbot.views.form.section import show_section, show_section_completed, show_section_fields

"""
    "section.section_id": section_id,
    "section.field_id": field_id,

    "form.form_id": form_id,
    "form.form_step": form_step,
    "form.section_step": section_step,
    "form.data.{section_id}.{field_id}": value
    ...
"""


class EditSectionScene(Scene, state="edit_section"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               section_id: str) -> None:

        section = deps.forms.get_section(section_id)
        data = await state.update_data({"section.section_id": section_id,
                                        "section.field_id": None})
        section_data = sub_dict_by_prefix(data, prefix=f"form.data.{section_id}.")
        await show_section(section, section_data, message=message)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      section_id: str) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(
                query.message, state, deps, section_id=section_id)


    @on.callback_query(F.data)
    async def section_actions_callback(self,
                                       query: CallbackQuery,
                                       state: FSMContext,
                                       deps: Dependencies,
                                       bot: Bot) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            data = await state.get_data()
            section_id = data["section.section_id"]
            section = deps.forms.get_section(section_id)
            if query.data.startswith("section:"):
                _, action = query.data.split(":")
                match action:
                    case "confirm":
                        # Remove section keyboard
                        await bot.edit_message_reply_markup(
                            chat_id=query.from_user.id,
                            message_id=query.message.message_id,
                            reply_markup=None)
                        await show_section_completed(query.message)
                        await asyncio.sleep(0.5)
                        # Switch form step
                        form_id = data["form.form_id"]
                        form_step = data.get("form.form_step", 0)
                        data["form.form_step"] = form_step + 1
                        data["form.section_step"] = 0
                        await state.set_data(data)
                        # Go back to form scene
                        await self.wizard.goto("fill_form", form_id=form_id)
                    case "edit":
                        await show_section_fields(section, message=query.message)
            if query.data.startswith("field:"):
                _, field_id = query.data.split(":")
                data["section.field_id"] = field_id
                await state.set_data(data)
                field = deps.forms.get_field(field_id)
                value = data[f"form.data.{section_id}.{field_id}"]
                await show_field_input(field, value, message=query.message, replace=True)


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext,
                            deps: Dependencies) -> None:
        if message.text:
            data = await state.get_data()
            section_id = data["section.section_id"]
            field_id = data.get("section.field_id", None)
            if field_id and isinstance(field_id, str):
                field = deps.forms.get_field(field_id)
                if message.text == ALL:
                    await show_all_options(field, message=message)
                    return
                try:
                    value = deps.forms.validate_field_input(field, message.text)
                except ValidationError as error:
                    await message.answer(str(error))
                else:
                    data[f"form.data.{section_id}.{field_id}"] = value
                    data["section.field_id"] = None
                    await state.set_data(data)
                    await self.wizard.retake(section_id=section_id)