import asyncio

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import BufferedInputFile, CallbackQuery, InputMediaPhoto, Message
from uuid_extensions import uuid7

from src.deps import Dependencies
from src.entities.choices import Country
from src.entities.passport import PassportFiles
from src.entities.recognition import RecognitionResult
from src.tgbot.utils.helpers import sub_dict_by_prefix
from src.tgbot.views.visa.visa import check_passport_kb, visa_country_kb, visa_type_kb

VISA_COUNTRY_TEXT = "В какую страну вам нужна виза?"
VISA_TYPE_TEXT = "Выберите тип визы"
PASSPORT_TEXT = "Отправьте фото загранпаспорта"
CHECK_PASSPORT = "Вот немного улучшенное фото. Убедитесь, что вся информация читается и нет бликов"
WAITING_TEXT = "Пожалуйста, подождите..."

class ApplyVisaScene(Scene, state="apply_visa"):

    @on.message.enter()
    async def message_on_enter(self, message: Message, state: FSMContext) -> None:
        require_passport = False
        data = await state.get_data()
        if data.get("visa.data.country", None) is None:
            await message.answer(VISA_COUNTRY_TEXT, reply_markup=visa_country_kb())
        elif data.get("visa.data.type", None) is None:
            await message.answer(VISA_TYPE_TEXT, reply_markup=visa_type_kb())
        elif require_passport and data.get("visa.data.attachment_id", None) is None:
            data["visa.expecting"] = "passport"
            await state.set_data(data)
            await message.answer(PASSPORT_TEXT)
        elif data.get("form.form_step", None) is None:
            visa_type = data["visa.data.type"].split("_")[0]    # tour/business
            form_id = data["visa.data.country"] + "_" + visa_type
            await self.wizard.goto("fill_form", form_id=form_id)
        else:
            await self.wizard.exit()


    @on.callback_query.enter()
    async def callback_query_on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message, state)


    @on.callback_query(F.data)
    async def visa_data_update_callback(self, query: CallbackQuery, state: FSMContext) -> None:
        if query.data.startswith("visa_data:"):
            _, key, value = query.data.split(":")
            await state.update_data({f"visa.data.{key}": value})
            await self.wizard.retake()
        elif query.data.startswith("passport_checked"):
            _, checked = query.data.split(":")
            if checked == "no":
                await state.update_data({"visa.data.attachment_id": None})
            await self.wizard.retake()


    @on.message(F.photo)
    async def process_photo(self,
                            message: Message,
                            bot: Bot,
                            state: FSMContext,
                            deps: Dependencies) -> None:
        data = await state.get_data()
        is_expecting = data.get("visa.expecting", None)
        if message.photo and is_expecting == "passport":
            wait_message = await message.answer(WAITING_TEXT)
            photo = await bot.download(message.photo[-1])
            data = bytes(photo.read())
            # Recognition start
            recognition_id = str(uuid7())
            await deps.attachments.add_bytes(recognition_id, PassportFiles.SOURCE, data)
            result_dict = await deps.rpc.proxy.recognize_passport(id_=recognition_id)
            result = RecognitionResult(**result_dict)
            scanned = await deps.attachments.get_bytes(recognition_id, PassportFiles.SCANNED)
            # Recognition end
            await wait_message.delete()
            details = result.details
            lines = [
                f"<b>Фамилия:</b> {details.surname}",
                f"<b>Имя:</b> {details.given_name}",
                f"<b>Пол:</b> {details.gender}",
                f"<b>Дата рождения:</b> {details.birth_date}",
                f"<b>Место рождения:</b> {details.birth_place}",
                f"<b>Номер паспорта:</b> {details.passport_no}",
                f"<b>Страна выдачи:</b> {details.country}",
                f"<b>Дата выдачи:</b> {details.issue_date}",
                f"<b>Действителен до:</b> {details.expire_date}",
            ]
            output = "\n".join(lines)
            await message.answer(output)
            await message.answer_photo(
                BufferedInputFile(scanned, PassportFiles.SCANNED),
                caption=CHECK_PASSPORT,
                reply_markup=check_passport_kb(),
            )
            await state.update_data({
                "visa.data.attachment_id": recognition_id,
                "passport_details.surname": details.surname,
                "passport_details.given_name": details.given_name,
                "passport_details.gender": details.gender,
                "passport_details.birth_date": str(details.birth_date),
                "passport_details.birth_place": details.birth_place,
                "passport_details.passport_no": details.passport_no,
                "passport_details.country": details.country,
                "passport_details.issue_date": str(details.issue_date),
                "passport_details.expire_date": str(details.expire_date),
            })


    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        visa_data = sub_dict_by_prefix(data, prefix="visa.data.")
        await message.answer(str(visa_data))
        passport_details = sub_dict_by_prefix(data, prefix="passport_details.")
        await message.answer(str(passport_details))
        form_data = sub_dict_by_prefix(data, prefix="form.data.")
        await message.answer(str(form_data))
