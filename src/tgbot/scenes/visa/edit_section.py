import asyncio

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.exceptions import ValidationError
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.buttons import ALL, NO
from src.tgbot.views.form.field import show_all_options, show_field_condition, show_field_input
from src.tgbot.views.form.section import show_section, show_section_completed, show_section_fields

"""
    "section.section_id": section_id,
    "section.field_id": field_id,

    "form.form_id": form_id,
    "form.form_step": form_step,
    "form.section_step": section_step,
    "form.data.{section_id}.{field_id}": value

    "field.check_condition": True,
    ...
"""


class EditSectionScene(Scene, state="edit_section"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               section_id: str | None = None) -> None:

        data = await state.get_data()
        if section_id is not None:
            # Set defaults
            data["section.section_id"] = section_id
            data["section.field_id"] = None
            data["field.check_condition"] = True
            await state.set_data(data)

        # Show template depending on state data
        section_id = data["section.section_id"]
        field_id = data["section.field_id"]
        check_condition = data["field.check_condition"]

        if field_id is None:
            section = deps.forms.get_section(section_id)
            section_data = sub_dict_by_prefix(data, prefix=f"form.data.{section_id}.")
            await show_section(section, section_data, message=message)
        else:
            field = deps.forms.get_field(field_id)
            if check_condition and field.is_optional:
                await show_field_condition(field, message=message, replace=True)
            else:
                value = data[f"form.data.{section_id}.{field_id}"]
                await show_field_input(field, value, message=message, replace=True)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      section_id: str | None = None) -> None:
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

            if query.data.startswith("section:"):
                _, action = query.data.split(":")
                data = await state.get_data()
                match action:

                    case "confirm":
                        # Remove section keyboard
                        await bot.edit_message_reply_markup(
                            chat_id=query.from_user.id,
                            message_id=query.message.message_id,
                            reply_markup=None)
                        await show_section_completed(query.message)
                        await asyncio.sleep(0.3)
                        # Switch form step
                        data["form.form_step"] = data["form.form_step"] + 1
                        data["form.section_step"] = 0
                        await state.set_data(data)
                        # Go back to form scene
                        await self.wizard.goto("fill_form")

                    case "edit":
                        section_id = data["section.section_id"]
                        section = deps.forms.get_section(section_id)
                        await show_section_fields(section, message=query.message)

            elif query.data.startswith("field:"):
                _, field_id = query.data.split(":")
                await state.update_data({"section.field_id": field_id})
                await self.wizard.retake()


    @on.message(F.text)
    async def process_input(self,
                            message: Message,
                            state: FSMContext,
                            deps: Dependencies) -> None:

        if message.text:
            data = await state.get_data()

            section_id = data["section.section_id"]
            field_id = data["section.field_id"]
            check_condition = data["field.check_condition"]

            field = deps.forms.get_field(field_id)

            if message.text == ALL:
                await show_all_options(field, message=message)
                return

            if check_condition and field.is_optional:
                if message.text == NO:
                    value = None
                else:
                    data["field.check_condition"] = False
                    await state.set_data(data)
                    await self.wizard.retake()
                    return

            else:
                try:
                    value = deps.forms.validate_input(field, message.text)
                except ValidationError as error:
                    await message.answer(str(error))
                    return

            data[f"form.data.{section_id}.{field_id}"] = value
            data["section.field_id"] = None
            data["field.check_condition"] = True
            await state.set_data(data)
            await self.wizard.retake()
