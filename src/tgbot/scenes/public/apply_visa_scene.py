import asyncio
from uuid import UUID

from aio_pika import MessageProcessError
from aio_pika.patterns.rpc import JsonRPCError
from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from transliterate import translit
from uuid_extensions import uuid7

from src.deps import Dependencies
from src.entities.users import User
from src.entities.visas import AppFormAdd, AppFormUpdate, Country
from src.entities.visas.passport import PassportDetails, PassportFiles
from src.tgbot.views.menu import show_menu
from src.tgbot.views.visas.app_form import show_app_form
from src.tgbot.views.visas.apply_visa import (
    CHECKED_TEXT,
    CORNER_DETECTION_ERROR_TEXT,
    IMAGE_MISMATCH_ERROR_TEXT,
    PASSPORT_TEXT,
    START_TEXT,
    TEXT_RECOGNITION_ERROR_TEXT,
    WAITING_TEXT,
    show_check_passport_step,
    show_country_step,
    show_send_passport_step,
    show_visa_terms_step,
    show_visa_type_step,
)


class ApplyVisaScene(Scene, state="apply_visa"):

    @on.message.enter()
    async def message_on_enter(self,  # noqa: PLR0913
                               message: Message,
                               state: FSMContext, *,
                               deps: Dependencies,
                               current_user: User,
                               require_passport: bool = True) -> None:

        data = await state.get_data()
        service = deps.get_my_app_forms_service(current_user)
        visa_service = deps.get_visa_service()
        form_service = deps.get_forms_service()

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
            form = form_service.get_form(visa.form_id)
            await show_visa_terms_step(visa, form, message=message)

        elif data.get("visa.app_form_id") is None:
            await message.edit_reply_markup(reply_markup=None)
            app_form = await service.new_form(
                                AppFormAdd(user_id=current_user.id,
                                           country=data["visa.country"],
                                           visa_id=data["visa.visa_id"],
                                           data={}))
            data["visa.app_form_id"] = str(app_form.id)
            await state.set_data(data)
            await message.answer(START_TEXT)
            await asyncio.sleep(0.3)
            await self.wizard.retake()

        elif data.get("visa.passport_expecting") is None:
            if require_passport:
                await message.answer(PASSPORT_TEXT)
                data["visa.passport_expecting"] = True
                await state.set_data(data)
                await show_send_passport_step(message=message)
            else:
                data["visa.passport_expecting"] = False
                await state.set_data(data)
                await self.wizard.retake()
            id_ = UUID(data["visa.app_form_id"])
            await service.update_form(id_, AppFormUpdate(data=data))

        elif data.get("form.completed") is None:
            visa_id = data["visa.visa_id"]
            visa = visa_service.get_visa(visa_id)
            await self.wizard.goto("visa_form", form_id=visa.form_id)

        else:
            id_ = UUID(data["visa.app_form_id"])
            await service.update_form(id_, AppFormUpdate(data=data))
            await service.save_form(id_)
            await self.wizard.goto("my_app_form", id_=data["visa.app_form_id"], back=False)



    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: Dependencies,
                                      current_user: User) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(message=query.message,
                                        state=state,
                                        deps=deps,
                                        current_user=current_user)


    @on.callback_query(F.data)
    async def visa_data_update_callback(self,
                                        query: CallbackQuery,
                                        state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            match query.data:
                case "back":
                    await state.update_data({"visa.terms_accepted": None})
                    await self.wizard.retake()

                case "continue":
                    await state.update_data({"visa.terms_accepted": True})
                    await self.wizard.retake()

                case query.data if query.data.startswith("visa:"):
                    _, key, value = query.data.split(":")
                    await state.update_data({f"visa.{key}": value})
                    await self.wizard.retake()

                case query.data if query.data.startswith("passport:"):
                    _, checked = query.data.split(":")
                    if checked == "retry":
                        await state.update_data({"visa.passport_expecting": None})
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
        expecting = data.get("visa.passport_expecting")
        if message.photo and expecting:
            wait_message = await message.answer(WAITING_TEXT)
            photo = await bot.download(message.photo[-1])
            data = bytes(photo.read())
            # Recognition start
            attachment_id = uuid7()
            attachment_service = deps.get_my_attachments_service(current_user)
            await attachment_service.add_bytes(attachment_id, PassportFiles.SOURCE, data)
            # aio_pika.exceptions.MessageProcessError
            try:
                result_dict = await deps.rpc.proxy.recognize_passport(id_=str(attachment_id))
            except JsonRPCError as e:
                error_type = e.args[1]["error"]["type"]
                await wait_message.delete()
                match error_type:
                    case "ImageMismatchError":
                        await message.answer(IMAGE_MISMATCH_ERROR_TEXT)
                    case "CornerDetectionError":
                        await message.answer(CORNER_DETECTION_ERROR_TEXT)
                    case "TextRecognitionError":
                        await message.answer(TEXT_RECOGNITION_ERROR_TEXT)
                    case _:
                        raise
                return
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
            birth_place = str(details.birth_place).replace("ГОР.", "").replace("Г.", "").strip().upper()
            birth_place = translit(birth_place, "ru", reversed=True)
            await state.update_data({
                "visa.passport_expecting": False,
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
