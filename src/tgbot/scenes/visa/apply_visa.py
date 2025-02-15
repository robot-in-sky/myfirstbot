import asyncio

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from transliterate import translit
from uuid_extensions import uuid7

from src.deps import Dependencies
from src.entities.visa.passport import PassportDetails, PassportFiles
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.visa.visa import (
    PASSPORT_AGAIN,
    PASSPORT_CHECKED_TEXT,
    WAITING_TEXT,
    show_check_passport_step,
    show_country_step,
    show_passport_step,
    show_visa_info,
    show_visa_type_step,
)


class ApplyVisaScene(Scene, state="apply_visa"):

    @on.message.enter()
    async def message_on_enter(self, message: Message, state: FSMContext, *,
                               require_passport: bool = True) -> None:
        data = await state.get_data()
        if data.get("visa.data.country", None) is None:
            await show_country_step(message=message)
        elif data.get("visa.data.type", None) is None:
            await show_visa_type_step(message=message)
        elif data.get("visa.data.attachment_id", None) is None:
            visa_data = sub_dict_by_prefix(data, prefix="visa.data.")
            await show_visa_info(visa_data, message=message)
            await asyncio.sleep(0.3)
            if require_passport:
                data["visa.expecting"] = "passport"
                await state.set_data(data)
                await show_passport_step(message=message)
            else:
                data["visa.data.attachment_id"] = "***"
                await state.set_data(data)
                await self.wizard.retake()
        elif data.get("form.form_step", None) is None:
            visa_type = data["visa.data.type"].split("_")[0]    # tour/business
            form_id = data["visa.data.country"] + "_" + visa_type
            await self.wizard.goto("fill_form", form_id=form_id)
        else:
            visa_data = sub_dict_by_prefix(data, prefix="visa.data.")
            await message.answer(str(visa_data))
            form_data = sub_dict_by_prefix(data, prefix="form.data.")
            await message.answer(str(form_data))
            await self.wizard.exit()


    @on.callback_query.enter()
    async def callback_query_on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message, state)


    @on.callback_query(F.data)
    async def visa_data_update_callback(self, query: CallbackQuery, state: FSMContext, bot: Bot) -> None:
        if query.data.startswith("visa_data:"):
            _, key, value = query.data.split(":")
            await state.update_data({f"visa.data.{key}": value})
            await self.wizard.retake()
        elif query.data.startswith("passport_checked:"):
            await query.answer()
            if isinstance(query.message, Message):
                _, checked = query.data.split(":")
                if checked == "no":
                    await state.update_data({"visa.data.attachment_id": None})
                    await query.message.answer(PASSPORT_AGAIN)
                    await query.message.delete()
                if checked == "yes":
                    # Remove section keyboard
                    await bot.edit_message_reply_markup(
                        chat_id=query.from_user.id,
                        message_id=query.message.message_id,
                        reply_markup=None)
                    await query.message.answer(PASSPORT_CHECKED_TEXT)
                await self.wizard.retake()


    @on.message(F.photo)
    async def process_photo(self,
                            message: Message,
                            bot: Bot,
                            state: FSMContext,
                            deps: Dependencies) -> None:
        data = await state.get_data()
        expecting = data.get("visa.expecting", None)
        if message.photo and expecting == "passport":
            wait_message = await message.answer(WAITING_TEXT)
            photo = await bot.download(message.photo[-1])
            data = bytes(photo.read())
            # Recognition start
            recognition_id = str(uuid7())
            await deps.attachments.add_bytes(recognition_id, PassportFiles.SOURCE, data)
            result_dict = await deps.rpc.proxy.recognize_passport(id_=recognition_id)
            scanned = await deps.attachments.get_bytes(recognition_id, PassportFiles.SCANNED)
            # Recognition end
            await wait_message.delete()
            details = PassportDetails(**result_dict["details"])
            """
            lines = [
                f"<b>Фамилия:</b> {details.surname}",
                f"<b>Имя:</b> {details.given_name}",
                f"<b>Пол:</b> {details.gender}",
                f"<b>Дата рождения:</b> {details.birth_date}",
                f"<b>Место рождения:</b> {details.birth_place}",
                f"<b>Номер паспорта:</b> {details.passport_no}",
                f"<b>Страна выдачи:</b> {details.country}",
                f"<b>Дата выдачи:</b> {details.issue_date}",
                f"<b>Действителен до:</b> {details.expiry_date}",
            ]
            output = "\n".join(lines)
            await message.answer(output)
            """
            birth_place = str(details.birth_place).replace("ГОР.", "").strip().upper()
            birth_place = translit(birth_place, "ru", reversed=True)
            await state.update_data({
                "visa.data.attachment_id": recognition_id,
                "form.data.registration.nationality": str(details.country).lower(),
                "form.data.applicant_details.surname": str(details.surname).upper(),
                "form.data.applicant_details.given_name": str(details.given_name).upper(),
                "form.data.applicant_details.gender": str(details.gender).lower(),
                "form.data.applicant_details.birth_date": str(details.birth_date),
                "form.data.applicant_details.birth_place": birth_place,
                "form.data.applicant_details.birth_country": str(details.country).lower(),
                "form.data.passport_details.passport_no": str(details.passport_no).upper(),
                "form.data.passport_details.passport_issue_date": str(details.issue_date),
                "form.data.passport_details.passport_expiry_date": str(details.expiry_date),
            })
            await show_check_passport_step(
                photo=BufferedInputFile(scanned, PassportFiles.SCANNED), message=message)


    @on.message.exit()
    async def message_on_exit(self, state: FSMContext) -> None:
        await state.set_data({})


    @on.callback_query.exit()
    async def callback_query_on_exit(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        await self.message_on_exit(state)
