from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Message

from src.entities.visas import Country, Visa, VisaType
from src.services.public.forms import COUNTRY_OUTPUT
from src.tgbot.views.buttons import BACK, CONTINUE, TO_MENU

VISA_COUNTRY_TEXT = ("<b>Виза какой страны вас интересует?</b>\n\n"
                     "Доступны следующие страны:")

VISA_TYPE_TEXT = "Выберите тип визы"

VISA_TERMS_TEXT = ("\n\n Для подачи заявки необходимо:\n"
                   "📋 Ответить на вопросы анкеты\n"
                   "🪪 Предоставить фото/скан паспорта (загран)\n"
                   "💳 Оплатить полную стоимость визы\n\n"
                   "В стоимость входит оплата консульского сбора и услуга заполнения\n\n"
                   'Нажимая "<b>Продолжить</b>", Вы даёте согласие на обработку персональных данных')

PASSPORT_TEXT = "Итак, начнём с паспорта\n\n"
SEND_PASSPORT_TEXT = ("<b>Сделайте фото разворота паспорта (загран):</b>\n\n"
                      "• Вертикальное фото без бликов\n"
                      "• Ровная поверхность\n"
                      "• Все углы должны быть в кадре\n"
                      "• Все надписи должны читаться\n"
                      "• Желательно темный фон\n\n"
                      "📎 Прикрепите фото к сообщению и отправьте")

CHECK_PASSPORT_TEXT = ("Вот фото после обработки\n"
                       "<b>Нажмите на фото, чтобы увеличить</b>\n\n"
                       "Убедитесь, что вся информация хорошо читается")

CHECKED_TEXT = "✅ Принято"
WAITING_TEXT = "Пожалуйста, подождите..."
START_TEXT = "🚀 Поехали!"

# COUNTRY
async def show_country_step(countries: Sequence[Country], *,
                            message: Message) -> Message:
    return await message.edit_text(VISA_COUNTRY_TEXT,
                                    reply_markup=visa_country_kb(countries))


def visa_country(country: Country) -> str:
    flag = {
        Country.IND: "🇮🇳",
        Country.VNM: "🇻🇳",
    }.get(country, "")
    output = COUNTRY_OUTPUT.get(country, country)
    return f"{flag} {output}" if flag else output


def visa_country_kb(countries: Sequence[Country]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                                    text=visa_country(country),
                                    callback_data=f"visa:country:{country}")] for country in countries])

# VISA TYPE
async def show_visa_type_step(visas: Sequence[Visa], *,
                              message: Message) -> Message:
    return await message.edit_text(VISA_TYPE_TEXT,
                                   reply_markup=visa_type_kb(visas))


def visa_type(type_: VisaType) -> str:
    return {
        VisaType.TOURIST: "Туристическая",
        VisaType.BUSINESS: "Бизнес",
        VisaType.MEDICAL: "Медицинская",
    }.get(type_, type_)


def visa_period(period: str) -> str:
    value, unit = period[:-1], period[-1]
    digit = int(value[-1])
    units = (unit, unit, unit)
    match unit:
        case "h":
            units = ("час", "часа", "часов")
        case "d":
            units = ("день", "дня", "дней")
        case "m":
            units = ("мес", "мес", "мес")
        case "y":
            units = ("год", "года", "лет")
    if digit == 1:
        unit = units[0]
    elif digit in (2, 3):
        unit = units[1]
    else:
        unit = units[2]
    return f"{value} {unit}"


def visa_type_kb(visas: Sequence[Visa]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                                    text=f"{visa_type(visa.type)} {visa_period(visa.period)}",
                                    callback_data=f"visa:visa_id:{visa.id}")] for visa in visas])


# VISA TERMS
async def show_visa_terms_step(visa: Visa, message: Message) -> Message:
    text = "<b>Оформление визы\n\n</b>".upper()
    text += await visa_summary(visa)
    text += VISA_TERMS_TEXT
    return await message.edit_text(text,
                                   reply_markup=visa_terms_kb())


async def visa_summary(visa: Visa) -> str:
    return (f"<b>Страна</b>: {visa_country(visa.country)}\n"
            f"<b>Тип визы</b>: {visa_type(visa.type)}\n"
            f"<b>Срок действия</b>: {visa_period(visa.period)}\n"
            f"<b>Стоимость</b>: {visa.price:.0f}₽\n"
            f"<b>Срок подачи заявки</b>: {visa_period(visa.app_period)}\n"
            f"<b>Срок обработки заявки</b>: {visa.proc_days_min}-{visa_period(f'{visa.proc_days_max}d')}")


def visa_terms_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=TO_MENU, callback_data="to_menu"),
        InlineKeyboardButton(text=CONTINUE, callback_data="continue")]])


# SEND PASSPORT
async def show_send_passport_step(message: Message) -> None:
    await message.answer(SEND_PASSPORT_TEXT,
                         reply_markup=send_passport_kb())


def send_passport_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=BACK, callback_data="back")]])


async def show_check_passport_step(photo: InputFile | str, *, message: Message) -> Message:
    return await message.answer_photo(
        photo=photo,
        caption=CHECK_PASSPORT_TEXT,
        reply_markup=check_passport_kb())


def check_passport_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Ещё раз", callback_data="passport:retry"),
        InlineKeyboardButton(text="✅ OK", callback_data="passport:ok")]])
