import asyncio

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from transliterate import translit
from uuid_extensions import uuid7

from src.deps import Dependencies
from src.entities.users import User
from src.entities.visas import Country
from src.entities.visas.passport import PassportDetails, PassportFiles
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.menu import show_menu
from src.tgbot.views.visas.visa_app import (
    CHECKED_TEXT,
    START_TEXT,
    WAITING_TEXT,
    show_check_passport_step,
    show_country_step,
    show_send_passport_step,
    show_visa_terms_step,
    show_visa_type_step, PASSPORT_TEXT,
)


class ApplyVisaScene(Scene, state="apply_visa"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext, *,
                               deps: Dependencies,
                               require_passport: bool = True) -> None:

        data = await state.get_data()
        visa_service = deps.get_visa_service()

        if data.get("visa.country") is None:
            countries = visa_service.get_countries()
            await show_country_step(countries, message=message)

        elif data.get("visa.visa_id") is None:
            country = data["visa.country"]
            visas = visa_service.get_visas_by_country(Country(country))
            await show_visa_type_step(visas, message=message)

        elif data.get("visa.terms_accepted") is None:
            visa_id = data["visa.visa_id"]
            visa = visa_service.get_visa(visa_id)
            await show_visa_terms_step(visa, message=message)

        elif data.get("visa.attachment_id") is None:
            await asyncio.sleep(0.3)
            if require_passport:
                if data.get("visa.expecting") is None:
                    await message.answer(PASSPORT_TEXT)
                data["visa.expecting"] = "passport"
                await state.set_data(data)
                await show_send_passport_step(message=message)
            else:
                data["visa.attachment_id"] = "***"
                await state.set_data(data)
                await self.wizard.retake()

        elif data.get("form.form_step") is None:
            visa_id = data["visa.visa_id"]
            visa = visa_service.get_visa(visa_id)
            await self.wizard.goto("form", form_id=visa.form_id)

        else:
            visa_data = sub_dict_by_prefix(data, prefix="visa.")
            await message.answer(str(visa_data))
            form_data = sub_dict_by_prefix(data, prefix="form.data.")
            await message.answer(str(form_data))
            await self.wizard.exit()


    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: Dependencies) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(message=query.message,
                                        state=state,
                                        deps=deps)


    @on.callback_query(F.data)
    async def visa_data_update_callback(self,
                                        query: CallbackQuery,
                                        state: FSMContext, *,
                                        current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):

            if query.data == "back":
                await state.update_data({"visa.terms_accepted": None})
                await self.wizard.retake()

            elif query.data == "to_menu":
                await self.wizard.exit()
                await show_menu(current_user=current_user,
                                message=query.message,
                                replace=True)

            elif query.data == "continue":
                await state.update_data({"visa.terms_accepted": True})
                await query.message.edit_reply_markup(reply_markup=None)
                await query.message.answer(START_TEXT)
                await self.wizard.retake()

            elif query.data.startswith("visa:"):
                _, key, value = query.data.split(":")
                await state.update_data({f"visa.{key}": value})
                await self.wizard.retake()

            elif query.data.startswith("passport:"):
                _, checked = query.data.split(":")
                if checked == "retry":
                    await state.update_data({"visa.attachment_id": None})
                    await query.message.delete()
                if checked == "ok":
                    await query.message.edit_reply_markup(reply_markup=None)
                    await query.message.answer(CHECKED_TEXT)
                await self.wizard.retake()


    @on.message(F.photo)
    async def process_photo(self,  # noqa: PLR0913
                            message: Message,
                            state: FSMContext, *,
                            bot: Bot,
                            deps: Dependencies,
                            current_user: User) -> None:
        data = await state.get_data()
        expecting = data.get("visa.expecting", None)
        if message.photo and expecting == "passport":
            wait_message = await message.answer(WAITING_TEXT)
            photo = await bot.download(message.photo[-1])
            data = bytes(photo.read())
            # Recognition start
            attachment_id = uuid7()
            attachment_service = deps.get_my_attachments_service(current_user)
            await attachment_service.add_bytes(attachment_id, PassportFiles.SOURCE, data)
            # aio_pika.exceptions.MessageProcessError
            result_dict = await deps.rpc.proxy.recognize_passport(id_=str(attachment_id))
            scanned = await attachment_service.get_bytes(attachment_id, PassportFiles.SCANNED)
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
                "visa.attachment_id": str(attachment_id),
                "visa.expecting": None,
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
