from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Message

from src.entities.visa import VisaType
from src.services.forms.choices.country import COUNTRY_OUTPUT

VISA_COUNTRY_TEXT = "В какую страну вам нужна виза?"
VISA_TYPE_TEXT = "Выберите тип визы"
PASSPORT_TEXT = "Отправьте фото загранпаспорта"
PASSPORT_EMOJI = "🪪"
CHECK_PASSPORT_TEXT = ("Вот немного улучшенное фото\n"
                       "<b>Нажмите на фото, чтобы увеличить</b>\n\n"
                       "Убедитесь, что вся информация читается и нет бликов")
PASSPORT_AGAIN = "Отправьте другое фото"
PASSPORT_CHECKED_TEXT = "✅ Принято"
WAITING_TEXT = "Пожалуйста, подождите..."


def visa_country_kb() -> InlineKeyboardMarkup:
    # TODO: The list of countries should not be hardcoded
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇮🇳 Индия", callback_data="visa_data:country:ind")]])


async def show_country_step(message: Message) -> Message:
    return await message.answer(VISA_COUNTRY_TEXT, reply_markup=visa_country_kb())


def visa_type(type_: VisaType) -> str:
    return {
        VisaType.TOUR_30D: "Туристическая 30 дней",
        VisaType.TOUR_1Y: "Туристическая 1 год",
        VisaType.TOUR_5Y: "Туристическая 5 лет",
    }.get(type_, type_)


def visa_type_kb() -> InlineKeyboardMarkup:
    # TODO: The types of visa should depend on the country chosen
    types = [VisaType.TOUR_30D, VisaType.TOUR_1Y, VisaType.TOUR_5Y]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=visa_type(type_),
                              callback_data=f"visa_data:type:{type_}")] for type_ in types])


async def show_visa_type_step(message: Message) -> Message:
    return await message.edit_text(VISA_TYPE_TEXT, reply_markup=visa_type_kb())


async def show_visa_info(data: dict[str: Any], message: Message) -> Message:
    lines = [
        f"<b>Страна</b>: {COUNTRY_OUTPUT.get(data.get("country"))}",
        f"<b>Тип визы</b>: {visa_type(data.get("type"))}",
        "\nПереходим к заполнению анкеты",
        "🚀 Поехали",
    ]
    text = "\n".join(lines)
    return await message.edit_text(text)


def check_passport_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Ещё раз", callback_data="passport_checked:no"),
        InlineKeyboardButton(text="✅ OK", callback_data="passport_checked:yes")]])


async def show_passport_step(message: Message) -> None:
    await message.answer(PASSPORT_TEXT)
    await message.answer(PASSPORT_EMOJI)


async def show_check_passport_step(photo: InputFile | str, *, message: Message) -> Message:
    return await message.answer_photo(
        photo=photo,
        caption=CHECK_PASSPORT_TEXT,
        reply_markup=check_passport_kb())
