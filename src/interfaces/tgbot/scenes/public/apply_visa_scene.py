import asyncio
from uuid import UUID

from aio_pika.patterns.rpc import JsonRPCError
from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from uuid_extensions import uuid7

from core.entities.users import User
from core.entities.visas import AppFormAdd, AppFormUpdate, Country
from core.entities.visas.passport import PassportDetails, PassportFiles
from core.services.utils.translate import format_place_name
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from interfaces.tgbot.utils.helpers import maybe_stringify
from interfaces.tgbot.views.visas.apply_visa import (
    CHECKED_TEXT,
    CORNER_DETECTION_ERROR_TEXT,
    IMAGE_MISMATCH_ERROR_TEXT,
    IMAGE_ONLY_ONE_TEXT,
    OCR_ERROR_TEXT,
    OCR_SUCCESS_TEXT,
    OCR_WARNING_TEXT,
    PASSPORT_TEXT,
    START_TEXT,
    WAITING_TEXT,
    show_check_passport_step,
    show_country_step,
    show_send_passport_step,
    show_visa_terms_step,
    show_visa_type_step,
)


class ApplyVisaScene(Scene, state="apply_visa"):

    @on.message.enter()
    async def message_on_enter(self,  # noqa: PLR0913, PLR0915
                               message: Message,
                               state: FSMContext, *,
                               deps: TgBotDependencies,
                               current_user: User,
                               require_passport: bool = True) -> None:

        data = await state.get_data()
        service = deps.get_my_app_forms_service(current_user)
        visa_service = deps.get_visa_service()
        survey_service = deps.get_survey_service()

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
            survey = survey_service.get_survey(visa.survey_id)
            await show_visa_terms_step(visa, survey, message=message)

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

        elif data.get("survey.completed") is None:
            await asyncio.sleep(0.3)
            if data.get("visa.ocr_success") == "True":
                await message.answer(OCR_SUCCESS_TEXT)
            elif data.get("visa.ocr_success") == "False":
                await message.answer(OCR_WARNING_TEXT)
            data["visa.ocr_success"] = None
            await state.set_data(data)
            await asyncio.sleep(0.3)
            visa_id = data["visa.visa_id"]
            visa = visa_service.get_visa(visa_id)
            await self.wizard.goto("survey", survey_id=visa.survey_id)

        else:
            id_ = UUID(data["visa.app_form_id"])
            await service.update_form(id_, AppFormUpdate(data=data))
            await service.save_form(id_)
            await self.wizard.goto("my_app_form", id_=data["visa.app_form_id"], back=False)



    @on.callback_query.enter()
    async def callback_query_on_enter(self,
                                      query: CallbackQuery,
                                      state: FSMContext, *,
                                      deps: TgBotDependencies,
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
                            deps: TgBotDependencies,
                            current_user: User) -> None:
        if message.media_group_id:
            await message.answer(IMAGE_ONLY_ONE_TEXT)
            return
        data = await state.get_data()
        expecting = data.get("visa.passport_expecting")
        if message.photo and expecting:
            wait_message = await message.answer(WAITING_TEXT)
            photo = await bot.download(message.photo[-1])
            photo_bytes = bytes(photo.read())
            # OCR start
            attachment_id = uuid7()
            attachment_service = deps.get_my_attachments_service(current_user)
            await attachment_service.add_bytes(attachment_id, PassportFiles.SOURCE, photo_bytes)
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
                        await message.answer(OCR_ERROR_TEXT)
                    case _:
                        raise
                return
            scanned = await attachment_service.get_bytes(attachment_id, PassportFiles.SCANNED)
            # OCR end
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
            birth_place = format_place_name(details.birth_place) if details.birth_place is not None else None
            details_dict = {
                "visa.passport_expecting": False,
                "survey.data.__passport_details__.nationality": maybe_stringify(details.country),
                "survey.data.__passport_details__.passport_no": maybe_stringify(details.passport_no),
                "survey.data.__passport_details__.surname": maybe_stringify(details.surname),
                "survey.data.__passport_details__.given_name": maybe_stringify(details.given_name),
                "survey.data.__passport_details__.gender": maybe_stringify(details.gender),
                "survey.data.__passport_details__.birth_date": maybe_stringify(details.birth_date),
                "survey.data.__passport_details__.birth_country": maybe_stringify(details.country),
                "survey.data.__passport_details__.birth_place": birth_place,
                "survey.data.__passport_details__.passport_issue_place": birth_place,
                "survey.data.__passport_details__.passport_issue_date": maybe_stringify(details.issue_date),
                "survey.data.__passport_details__.passport_expiry_date": maybe_stringify(details.expiry_date),
            }
            details_dict["visa.ocr_success"] = None not in details_dict.values()
            details_dict = {k: str(v) for k, v in details_dict.items() if v is not None}
            data = await state.update_data(details_dict)
            # Autosave
            service = deps.get_my_app_forms_service(current_user)
            id_ = UUID(data["visa.app_form_id"])
            await service.update_form(id_, AppFormUpdate(data=data))

            await show_check_passport_step(
                photo=BufferedInputFile(scanned, PassportFiles.SCANNED), message=message)
